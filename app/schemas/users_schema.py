from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = None

    class config:
        orm_mode = True


class UpdateUserSchema(BaseModel):
    username: str
    email: str

    class config:
        orm_mode = True

class GetUserSchema(UserSchema):
    id: int

    class config:
        orm_mode = True

class UserLoginSchema(BaseModel):
    email: str
    password: str
