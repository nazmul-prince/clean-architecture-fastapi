from typing import List, Optional

from pydantic import BaseModel

from app.core.schema.user_schema import UserSchema, RoleSchema


class UsersSchema(BaseModel):
    users: List[UserSchema]

class RolesSchema(BaseModel):
    users: List[RoleSchema]
    class Config:
        orm_mode = True
        form_attributes = True