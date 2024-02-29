from passlib.context import CryptContext
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password).encode('utf-8')

def authenticate_user(pseudo: str, password: str, db: Session):
    user = db.usersData.find_one({"pseudo": pseudo})
    if not user:
        return False
    if not verify_password(password, user["hashedPassword"]):
        return False
    return user