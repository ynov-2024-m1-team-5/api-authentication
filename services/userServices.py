from sqlalchemy.orm import Session
import schemas.users as schemas
import models.users as models
from fastapi import HTTPException
from services.utils import *
from config.settings import settings
import services.authServices as auth_service
from jose import jwt, exceptions 


def get_all_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter_by(id=customer_id).first()

def get_all_administrators(db: Session):
    return db.query(models.Administrator).all()

def get_administrator_by_id(db: Session, administrator_id: int):
    return db.query(models.Administrator).filter_by(id=administrator_id).first()

def get_all_usersLogin(db: Session):
    return db.query(models.UserLogin).all()

def get_userLogin_by_id(db: Session, userLogin:int):
    return db.query(models.UserLogin).filter_by(id=userLogin).first()

def customer_create(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    if db.query(models.Customer).filter_by(email=db_customer.email).first():
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )
    else:
        hashedPassword = get_password_hash(db_customer.password)
        userLogin = models.UserLogin(customer_id=db_customer.id, hashed_password=hashedPassword)
        db.add(db_customer)

        db.commit()

        hashedPassword = get_password_hash(db_customer.password)
        userLogin = models.UserLogin(
            customer_id=db_customer.id, 
            hashed_password=hashedPassword)
        db.add(userLogin)
        db.commit()

        db.refresh(userLogin)
        send_email(recipients=[settings.EMAIL_FROM],
                   subject="New Customer",
                   content=f"New customer on the platform : {db_customer.email}")
        send_email(recipients=[str(db_customer.email)], 
                   subject="Creation account",
                   content="Congrats!\n You have created an account on our platform.")
        return {"success": True, "customer_id": db_customer.id, "user_login": userLogin.id}


def administrator_create(db: Session, administrator: schemas.AdministratorCreate):
    if db.query(models.Administrator).filter_by(email=administrator.email).first():
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )
    else:
        db_administrator = models.Administrator(
            first_name=administrator.first_name,
            last_name=administrator.last_name,
            email=administrator.email)
        db.add(db_administrator)
        db.commit()
        hashedPassword = get_password_hash(administrator.password)
        adminLogin = models.AdminLogin(
            admin_id=db_administrator.id,
            password=hashedPassword) 
        db.add(adminLogin)
        db.commit()

        return {"success": True}

async def update_customer(db: Session, customer_id: int, updated_data: schemas.CustomerUpdate):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        for key, value in updated_data.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None

def update_administrator(db: Session, administrator_id: int, updated_data: schemas.AdministratorUpdate):
    db_administrator = db.query(models.Administrator).filter(models.Administrator.id == administrator_id).first()
    if db_administrator:
        for key, value in updated_data.model_dump().items():
            setattr(db_administrator, key, value)
        db.commit()
        db.refresh(db_administrator)
        return db_administrator
    return None

def delete_customer(customerDelete: schemas.CustomerDelete, db: Session):
    customer_delete_id = customerDelete.userLogin_id
    token = customerDelete.token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    if payload.get("is_admin"):
        db_customer = db.query(models.Customer).filter(models.Customer.id == customer_delete_id).first()
        if db_customer:
            db.delete(db_customer)
            db.commit()
            return True
    return False
