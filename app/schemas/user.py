from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, validator, root_validator, constr

class ItemBase(BaseModel):
    title: str 
    description: Optional[str] = None 

class ItemCreate(ItemBase):
    pass 

class Item(ItemBase):
    id: int 
    owner_id: int 

    class Config:
        orm_mode = True 

class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHERS = 'OTHERS'

class Address(BaseModel):
    street_address: Optional[str] = None
    postal_code: Optional[str] = None 
    city: Optional[str] = None 
    country: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr 
    gender: Gender
    address: Optional[Address] = None
    age: Optional[int] = Field(None, ge=18, le=25)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    batch_date: date

    @validator("batch_date")
    def valid_batch_date(cls, v: date):
        delta = date.today() - v 
        age = delta.days / 365 
        if age > 2:
            raise ValueError("Your batch seem a bit too old!")
        return v

    @validator("gender", pre=True)
    def join_values(cls, v: str):
        v_list = v.split(' ')
        if len(v_list) > 1:
            return ''.join(v_list)
        return v


class UserCreate(UserBase):
    password: str 
    password_confirmation: str
    
    def get_gender(self):
        return f"{self.gender[0]}"

    @root_validator()
    def password_match(cls, values):
        password = values.get('password')
        password_confirmation = values.get('password_confirmation')
        if password != password_confirmation:
            raise ValueError("Password don't match")
        return values

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    gender: Optional[Gender] = None
    address: Optional[Address] = None
    age: Optional[int] = Field(None, ge=18, le=25)
    batch_date: Optional[date] = None
    disable_date: Optional[date] = None




class User(UserBase):
    id: Optional[int]
    is_active: Optional[bool]
    disable_date: Optional[date]
    
    #items: List[Item] = [] 

    class Config:
        orm_mode = True 

class UserAll(UserBase):
    is_active: Optional[bool]
    disable_date: Optional[date]

    # class Config:
    #     orm_mode = True 

TestConstr = constr(regex=r'^\d{4}$')
