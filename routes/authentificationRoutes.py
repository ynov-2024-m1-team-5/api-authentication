from fastapi import APIRouter, Depends, HTTPException, status
from services import userServices as users_services
import services.authServices as auth_services
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.users import Base
from schemas.users import *
from schemas.token import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from config.settings import settings

Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

usersRoutes = APIRouter()
base = "/users"

@usersRoutes.get(f"{base}/usersLogin/")
def get_all_userslogin(db: Session=Depends(get_db)):
    return users_services.get_all_usersLogin(db)

@usersRoutes.get(f"{base}/usersLogin"+"/{id}")
def get_all_userslogin_by_id(id:int, db: Session=Depends(get_db)):
    return users_services.get_userLogin_by_id(db, id)

@usersRoutes.get(f"{base}/customers/",response_model=list[Customer],status_code=200)
def get_all_customers(db: Session = Depends(get_db)):
    return users_services.get_all_customers(db)

@usersRoutes.get(f"{base}/customers"+"/{id}")
def get_customer_by_id(id:int, db: Session = Depends(get_db)):
    return users_services.get_customer_by_id(db, id)

@usersRoutes.get(f"{base}/administrators/")
def get_all_administrators(db: Session = Depends(get_db)):
    return users_services.get_all_administrators(db)

@usersRoutes.get(f"{base}/administrators"+"/{id}")
def get_administrator_by_id(id:int, db: Session = Depends(get_db)):
    return users_services.get_administrator_by_id(db, administrator_id=id)

@usersRoutes.post(f"{base}/customers/")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return users_services.customer_create(db, customer)

@usersRoutes.post(f"{base}/administrators/")
def create_administrators(administrator: AdministratorCreate, db: Session = Depends(get_db)):
    users_services.administrator_create(db, administrator)
    return {"success": True}

@usersRoutes.patch(f"{base}/customers/" + "{id}", response_model= CustomerUpdate)
def update_customer(id: int, customer):
    pass

@usersRoutes.patch(f"{base}/administrators/" + "{id}", response_model= AdministratorUpdate)
def update_customer(id: int, customer):
    pass

@usersRoutes.delete(f"{base}/customers"+"/{id}")
def delete_customer(id: int, customer: CustomerDelete):
    pass

@usersRoutes.post(f"{base}/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    userlogin = auth_services.authenticate_user(db, form_data.username, form_data.password)
    if not userlogin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_services.create_access_token(
        data={"sub": userlogin.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@usersRoutes.get(f"{base}/me/")
def read_users_me(db: Session=Depends(get_db), current_user: UserLogin = Depends(auth_services.get_current_user)):
    return current_user
