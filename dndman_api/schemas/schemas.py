from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserSigninRequest(BaseModel):
    email: str
    password: str

class UserSignedIn(BaseModel):
    session: str
    user: int

class CharacterCreationRequestion(BaseModel):
    pass