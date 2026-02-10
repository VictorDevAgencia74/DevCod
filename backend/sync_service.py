import time
import requests
import sqlite3
import json
import os

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "sigf_local.db")

# Supabase Config (Placeholder - User needs to fill this)
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
TABLE_NAME = "checklists"

def get_unsynced_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, checklist_id, data, created_at FROM checklist_responses WHERE synced = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_as_synced(local_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE checklist_responses SET synced = 1 WHERE id = ?", (local_id,))
    conn.commit()
    conn.close()

def sync_to_supabase(row):
    local_id, checklist_id, data_json, created_at = row
    
    payload = {
        "checklist_id": checklist_id,
        "data": json.loads(data_json) if isinstance(data_json, str) else data_json,
        "created_at": created_at,
        "device_id": "tablet-01" # Example metadata
    }
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    try:
        response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", json=payload, headers=headers)
        if response.status_code in [200, 201]:
            print(f"✅ Synced ID {local_id}")
            mark_as_synced(local_id)
        else:
            print(f"❌ Failed ID {local_id}: {response.text}")
    except Exception as e:
        print(f"⚠️ Network Error: {e}")

def main():
    print("🚀 Starting SIGF Sync Service...")
    while True:
        rows = get_unsynced_data()
        if rows:
            print(f"Found {len(rows)} pending items...")
            for row in rows:
                sync_to_supabase(row)
        else:
            print("Nothing to sync. Sleeping...", end="\r")
        
        time.sleep(60) # Check every minute

if __name__ == "__main__":
    main()
