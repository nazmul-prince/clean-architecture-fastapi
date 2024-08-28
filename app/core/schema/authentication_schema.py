from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class TokenExchangeRequestSchema(BaseModel):
    subject_token: str

    class Config:
        orm_mode = True
        from_attributes = True

class NewTokenRequestSchema(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_token_expires_in: int
    refresh_token_expires_in: int
