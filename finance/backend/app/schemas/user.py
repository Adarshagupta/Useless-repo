from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None

class UserInDBBase(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str 