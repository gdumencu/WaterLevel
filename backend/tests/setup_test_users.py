from app.models.user import User
from app.dependencies import get_db
from core.security import get_password_hash  # or your hash function

def create_test_user(username: str, password: str, role: str = "user", email: str = "user@examle.com"):
    db = next(get_db())
    hashed_pw = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_pw, role=role, email=email)

    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created test user: {username}")

if __name__ == "__main__":
    print("Setting up test users...")   
    create_test_user("viewUser", "viewpass", "viewer", "testuser@example.com")
    print("Created test user: viewUser")    
    create_test_user("adminUser", "adminpass", "admin", "admin@example.com")
    print("Created test user: adminUser")   
    create_test_user("operatorUser", "operatorpass", "operator", "operator@example.com")
    print("Created test user: operatorUser")
    # Example User model fields for reference   
    # id = Column(Integer, primary_key=True)
    # username = Column(String(50), unique=True, nullable=False)
    # hashed_password = Column(String(128), nullable=False)
    # is_active = Column(Boolean, default=True)
    # email = Column(String(100), unique=True, nullable=False)
    # role = Column(String(20), nullable=False)