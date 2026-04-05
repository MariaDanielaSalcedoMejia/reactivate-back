from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    birth_date: Optional[date] = None
    age: Optional[int] = None

    @field_validator('birth_date', mode='before')
    @classmethod
    def calculate_birth_date_from_age(cls, v, info):
        # If birth_date is not provided, calculate it from age
        if v is None and info.data.get('age'):
            age = info.data.get('age')
            today = datetime.now().date()
            birth_date = date(today.year - age, today.month, today.day)
            return birth_date
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    birth_date: date | None = None
    role: str

    class Config:
        from_attributes = True
