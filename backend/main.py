import json
import os
import io
from typing import List, Optional, Any
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Body, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, JSON, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# import pandas as pd (Moved to inside function to avoid startup overhead/DLL issues)
from passlib.context import CryptContext
from jose import JWTError, jwt

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
SCHEMAS_DIR = os.path.join(BASE_DIR, "..", "schemas")
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'sigf_local.db')}"

# Auth Config (Phase 2 Prep)
SECRET_KEY = "SECRET_KEY_CHANGE_ME_IN_PRODUCTION" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Database Setup ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DB Models ---
class ChecklistResponse(Base):
    __tablename__ = "checklist_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(String, index=True) # Ex: CHK-VL-001
    data = Column(JSON) # Stores the form fields as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    synced = Column(Boolean, default=False) # For Supabase sync logic

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # 'driver', 'manager', 'mechanic'

Base.metadata.create_all(bind=engine)

# --- Security ---
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- FastAPI App ---
app = FastAPI(title="SIGF-Const PWA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic Models ---
class ChecklistSubmission(BaseModel):
    checklist_id: str
    data: dict

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

# --- Routes ---

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# 1. Config
@app.get("/api/schemas/checklists")
def get_checklists_schema(current_user: User = Depends(get_current_user)):
    """Returns the JSON configuration for dynamic forms."""
    try:
        with open(os.path.join(SCHEMAS_DIR, "checklists.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Checklist schema not found")

# 2. Submission (Create)
@app.post("/api/submit")
def submit_checklist(submission: ChecklistSubmission, db: Session = Depends(get_db)):
    """Receives filled form data and saves to SQLite."""
    try:
        db_item = ChecklistResponse(
            checklist_id=submission.checklist_id,
            data=submission.data,
            synced=False
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return {"status": "success", "id": db_item.id, "message": "Saved locally"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Read All (For Admin/History)
@app.get("/api/checklists")
def get_all_checklists(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Role-based filtering (optional): Drivers see own, Admins see all
    # For now, simplistic view
    items = db.query(ChecklistResponse).order_by(ChecklistResponse.created_at.desc()).all()
    return items

# 4. Update (For Admin CRUD)
@app.put("/api/checklists/{item_id}")
def update_checklist(item_id: int, submission: ChecklistSubmission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ['manager', 'admin']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    item = db.query(ChecklistResponse).filter(ChecklistResponse.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist not found")
    
    item.checklist_id = submission.checklist_id
    item.data = submission.data
    item.synced = False # Mark as unsynced so it updates cloud later
    db.commit()
    return {"status": "updated"}

# 5. Delete (For Admin CRUD)
@app.delete("/api/checklists/{item_id}")
def delete_checklist(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ['manager', 'admin']:
        raise HTTPException(status_code=403, detail="Not authorized")

    item = db.query(ChecklistResponse).filter(ChecklistResponse.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist not found")
    
    db.delete(item)
    db.commit()
    return {"status": "deleted"}

# 6. Excel Export (Phase 1)
@app.get("/api/export/excel")
def export_excel(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ['manager', 'admin', 'finance']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    try:
        from openpyxl import Workbook
    except ImportError:
         raise HTTPException(status_code=500, detail="openpyxl library not found")
    
    items = db.query(ChecklistResponse).all()
    if not items:
        raise HTTPException(status_code=404, detail="No data to export")
    
    # 1. Collect all dynamic keys to create consistent columns
    dynamic_keys = set()
    for item in items:
        if isinstance(item.data, dict):
            dynamic_keys.update(item.data.keys())
    
    sorted_keys = sorted(list(dynamic_keys))
    
    # 2. Create Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Checklists"
    
    # 3. Write Header
    headers = ["ID", "Tipo", "Data Criação", "Sincronizado"] + [f"Field_{k}" for k in sorted_keys]
    ws.append(headers)
    
    # 4. Write Rows
    for item in items:
        # Format date safely
        date_str = item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else ""
        
        row = [
            item.id,
            item.checklist_id,
            date_str,
            "Sim" if item.synced else "Não"
        ]
        
        # Add dynamic values
        if isinstance(item.data, dict):
            for k in sorted_keys:
                val = item.data.get(k, "")
                row.append(str(val)) # Ensure string for simplicity
        else:
             row.extend([""] * len(sorted_keys))
             
        ws.append(row)
    
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="relatorio_frota.xlsx"'
    }
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# 7. Auth Routes (Phase 2 Prep)
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Simple user creation for demo purposes
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    return {"username": user.username, "role": user.role}

@app.get("/api/sync-status")
def get_sync_status(db: Session = Depends(get_db)):
    """Stub for checking offline/online sync status."""
    pending_count = db.query(ChecklistResponse).filter(ChecklistResponse.synced == False).count()
    return {"pending_sync": pending_count}

# 8. Maintenance Module (Phase 3)
@app.get("/api/maintenance/alerts")
def get_maintenance_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Logic: Scan all latest checklists per vehicle, check if mileage > threshold
    # For MVP, we mock a rule: "Alert if any tire is CRITICAL"
    
    alerts = []
    items = db.query(ChecklistResponse).all()
    
    for item in items:
        data = item.data
        if isinstance(data, dict):
            # Rule 1: Tire Status
            if data.get("pneus") == "CRÍTICO":
                alerts.append({
                    "vehicle": data.get("placa", "Unknown"),
                    "issue": "Pneu Crítico",
                    "date": item.created_at
                })
            # Rule 2: Mileage (Example: > 10000)
            km = data.get("km_atual")
            if km and isinstance(km, (int, float)) and km > 10000:
                 alerts.append({
                    "vehicle": data.get("placa", "Unknown"),
                    "issue": "Revisão de 10.000km Vencida",
                    "date": item.created_at
                })

    return alerts

# Serve Frontend Static Files (PWA)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
