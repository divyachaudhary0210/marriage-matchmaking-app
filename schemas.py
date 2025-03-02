from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re



# Base User Schema with common attributes
class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: str
    city: str
    interests: str

    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 100:
            raise ValueError('Age must be between 18 and 100')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be Male, Female, or Other')
        return v

    @validator('email')
    def validate_email(cls, v):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v

# Schema for creating a User
class UserCreate(UserBase):
    pass

# Schema for updating a User
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[str] = None

    @validator('age')
    def validate_age(cls, v):
        if v is not None and (v < 18 or v > 100):
            raise ValueError('Age must be between 18 and 100')
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v is not None and v.lower() not in ['male', 'female', 'other']:
            raise ValueError('Gender must be Male, Female, or Other')
        return v

    @validator('email')
    def validate_email(cls, v):
        if v is not None:
            pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not re.match(pattern, v):
                raise ValueError('Invalid email format')
        return v

# Schema for returning a User
class User(UserBase):
    id: int

    class Config:
        orm_mode = True