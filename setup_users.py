from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import User, Base, get_password_hash, DATABASE_URL

# Setup DB Connection
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def create_initial_users():
    print("🚀 Criando usuários iniciais (Funcionários)...")
    
    # 1. Admin User
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        print("✅ Usuário 'admin' criado (Senha: admin123)")
    else:
        print("ℹ️ Usuário 'admin' já existe.")

    # 2. Driver User
    driver = db.query(User).filter(User.username == "motorista1").first()
    if not driver:
        driver_user = User(
            username="motorista1",
            hashed_password=get_password_hash("moto123"),
            role="driver"
        )
        db.add(driver_user)
        print("✅ Usuário 'motorista1' criado (Senha: moto123)")
    else:
        print("ℹ️ Usuário 'motorista1' já existe.")

    db.commit()
    db.close()
    print("🏁 Configuração de usuários concluída!")

if __name__ == "__main__":
    create_initial_users()
