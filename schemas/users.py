from pydantic import BaseModel

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
    id: int

class Customer(UserBase):
    id: int
    first_name: str
    last_name: str
    zipcode: str
    phone: str
    city: str
    
class AdministratorCreate(UserBase):
    firstName: str
    lastName: str
    password: str

class Administrator(UserBase):
    id: int


class AdministratorUpdate(AdministratorCreate):
    id: int

class CustomerDelete(BaseModel):
    userLogin_id: int
    token: str