from sqlalchemy.orm import Session
import schemas.users as schemas
import models.users as models
from fastapi import HTTPException
from services.utils import *


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
        print("Creating new user...")
        hashedPassword = get_password_hash(db_customer.password)
        userLogin = models.UserLogin(customer_id=db_customer.id, hashed_password=hashedPassword)
        db.add(userLogin)
        db.commit()

        hashedPassword = get_password_hash(db_customer.password)
        userLogin = models.UserLogin(
            customer_id=db_customer.id, 
            hashed_password=hashedPassword)
        db.add(userLogin)
        db.commit()

        db.refresh(userLogin)
        return {"success": True}


def administrator_create(db: Session, administrator: schemas.AdministratorCreate):
    db_administrator = models.Administrator(**administrator.model_dump())
    db.add(db_administrator)
    db.commit()
    db.refresh(db_administrator)
    return db_administrator

def update_customer(db: Session, customer_id: int, updated_data: schemas.CustomerUpdate):
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

def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return True
    return False
