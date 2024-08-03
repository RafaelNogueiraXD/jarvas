from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class AppPublic(BaseModel):
    id: int
    name: str
    description: str
    status: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]

class AppSchema(BaseModel):
    name: str
    description: str
    status: str

class AppList(BaseModel):
    apps: list[AppPublic]

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class AppMessage(BaseModel):
    name: str
    phone: str
