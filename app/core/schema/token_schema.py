from datetime import timedelta

from pydantic.v1 import BaseModel


class TokenSchema(BaseModel):
    access_token:str
    refresh_token:str
    expires_in:timedelta
    class Config:
        orm_mode = True
        form_attributes = True