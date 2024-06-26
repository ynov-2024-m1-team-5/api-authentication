from fastapi import APIRouter, Depends, HTTPException, status, Header
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
from typing import Union, Annotated

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


@usersRoutes.get(f"{base}/customers/", status_code=200)
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

@usersRoutes.patch(f"{base}/customers/" + "{id}", response_model= Customer)
async def update_customer(id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    return await users_services.update_customer(db, customer_id=id, updated_data=customer)

@usersRoutes.patch(f"{base}/administrators/" + "{id}", response_model= AdministratorUpdate)
def update_customer(id: int, customer):
    pass

@usersRoutes.delete(f"{base}/customers/"+ "{id}")
def delete_customer(customerDelete: CustomerDelete, db: Session = Depends(get_db)):
    return users_services.delete_customer(db=db, customerDelete=customerDelete)


@usersRoutes.post(f"{base}/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    res = auth_services.authenticate_user(db, form_data.username, form_data.password)
    try:
        userlogin = res[0]
        is_admin = res[1]
        customer = res[2]
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_services.create_access_token(
            data={"sub": str(userlogin.id), "is_admin": is_admin, "customer_id": customer.id}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    except:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@usersRoutes.get(f"{base}/me/")
def read_users_me(token:Annotated[Union[str, None], Header()] = None, db: Session=Depends(get_db)):
    return auth_services.get_current_user(token=token, db=db)
