from pydantic import BaseModel
from typing import Optional
class BaseModelExtend(BaseModel):
    class Config:
        from_attributes = True

class UserBase(BaseModelExtend):
    email: str

class UserLogin(UserBase):
    id : int
    
class CustomerCreate(UserBase):
    first_name: str
    last_name: str
    address: str
    zipcode: str
    phone: str
    city: str
    password: str

class CustomerCreateOut(UserBase):
    pass

class CustomerUpdate(CustomerCreate):
    first_name: Optional[str]
    last_name: Optional[str]
    zipcode: Optional[str]
    phone: Optional[str]
    city: Optional[str]
class Customer(UserBase):
    id: int
    first_name: str
    last_name: str
    zipcode: str
    phone: str
    city: str
    
class AdministratorCreate(UserBase):
    first_name: str
    last_name: str
    email: str
    password: str

class Administrator(UserBase):
    id: int


class AdministratorUpdate(AdministratorCreate):
    id: int

class CustomerDelete(BaseModel):
    userLogin_id: int
    token: str