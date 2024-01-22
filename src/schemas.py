from datetime import datetime, date

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    description: str
    birth_date: date
    created_at: datetime
    updated_at: datetime


class ResponseContactModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str
    surname: str
    email: EmailStr
    phone: str
    description: str | None
    birth_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str
    password: str