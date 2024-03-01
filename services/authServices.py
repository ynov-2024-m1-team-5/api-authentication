from sqlalchemy.orm import Session
from services.utils import *
from typing import Optional
from datetime import datetime, timedelta
from config.settings import settings
import models.users as models
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from schemas.token import TokenData
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/users/token")

def authenticate_user(db: Session, email: str, password: str):
    if not db.query(models.Customer).filter_by(email=email).first():
        user = db.query(models.Administrator).filter_by(email=email).first()
        login = db.query(models.AdminLogin).filter_by(admin_id=user.id).first()
        hashed_password = login.password
        is_admin = True
    else:
        user = db.query(models.Customer).filter_by(email=email).first()
        login = db.query(models.UserLogin).filter_by(customer_id=user.id).first()
        is_admin = False
        hashed_password = login.hashed_password 
    if not login:
        return {"detail": "Incorrect username or password"}
    if not verify_password(password, hashed_password):
        return {"detail": "Incorrect username or password"}
    return [login, is_admin]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(db, token: Annotated[str, Depends(oauth2_scheme)]):
    print("hehreee")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Customer).filter_by(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user