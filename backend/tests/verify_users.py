from app.dependencies import get_db
from app.models.user import User

def list_users():
    db = next(get_db())
    users = db.query(User).all()
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}, Role: {user.role}")

if __name__ == "__main__":
    list_users()
