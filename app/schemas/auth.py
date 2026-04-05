from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: EmailStr

    class Config:
        orm_mode = True
