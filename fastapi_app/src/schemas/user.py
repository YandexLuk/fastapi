from pydantic import BaseModel, Field, EmailStr, validator
import re
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)
    is_superuser: bool = Field(default=False, description="Флаг администратора")

    @validator('password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'[0-9]', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64)

    @validator('password')
    def validate_password_strength(cls, v):
        if v is not None:
            if not re.search(r'[A-Z]', v):
                raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
            if not re.search(r'[a-z]', v):
                raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
            if not re.search(r'[0-9]', v):
                raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class User(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool = False

    class Config:
        from_attributes = True