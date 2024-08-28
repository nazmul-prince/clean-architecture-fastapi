from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class UserAddressSchema(BaseModel):
    id: int
    division: Optional[str]
    zilla: Optional[str]
    upazilla: Optional[str]
    municipality: Optional[str]
    thana_union: Optional[str] = Field(None, alias="thanaUnion")
    ward: Optional[str]
    addr_ids: Optional[str] = Field(None, alias="addrIds")
    addr_details: Optional[str] = Field(None, alias="addrDetails")


class UserSchema(BaseModel):
    id: int | None = Field(default=None)
    username: str
    password: str
    name: Optional[str]
    office_id: Optional[int]
    email: str
    is_active:bool

class RoleSchema(BaseModel):
    id: int | None = Field(default=None)
    name: str
    description: str

class UserRoleSchema(BaseModel):
    id: int | None = Field(default=None)
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
        from_attributes = True
