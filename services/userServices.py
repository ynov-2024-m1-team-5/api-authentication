from sqlalchemy.orm import Session
import schemas.users as schemas
import models.users as models
from fastapi import HTTPException
from services.utils import *

def get_all_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_all_administrators(db: Session):
    administrators = db.query(models.Administrator).all()
    return {
        "len": len(administrators),
        "customers": administrators
    }

def get_administrator_by_id(db: Session, administrator_id: int):
    return db.query(models.Administrator).filter(models.Administrator.id == administrator_id).first()

def customer_create(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    if db.query(models.Customer).filter_by(email=db_customer.email).first():
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )
    else:
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)


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
