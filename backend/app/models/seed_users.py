# backend/app/models/seed_users.py

# Use absolute imports for scripts run as modules
from models.user import User
from models.audit_logs import AuditLog  # <-- This is critical!
from db.database import SessionLocal
from core.security import get_password_hash  # core is a sibling of models

db = SessionLocal()
users = [
    {"username": "admin", "password": "admin123"},
    {"username": "operator", "password": "operator123"},
    {"username": "viewer", "password": "viewer123"},
]

for u in users:
    try:
        existing_user = db.query(User).filter(User.username == u["username"]).first()
        if existing_user:
            print(f"User {u['username']} already exists. Skipping.")
            continue
        else:
            print(f"User {u['username']} does not exist. Creating...")
            db.add(User(
                username=u["username"],
                hashed_password=get_password_hash(u["password"]),
                role="admin" if u["username"] == "admin" else "operator" if u["username"] == "operator" else "viewer",
                email=f"{u['username']}@example.com"
            ))
            print(f"User {u['username']} created.") 
    except Exception as e:
        print(f"Error checking user {u['username']}: {e}")
        continue    

db.commit()
db.close()
print("User seeding completed.")
# Run this script with: python -m models.seed_users
# from the backend/app directory to ensure absolute imports work correctly.
