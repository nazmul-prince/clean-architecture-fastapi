from fastapi import FastAPI
from sqlalchemy import Column, Integer, String

from infradetails.model.base_mixin_model import BaseMixinModel, Base


class RoleModel(Base, BaseMixinModel):
    __tablename__ = "role"
    __table_args__ = {"schema": "event_management"}

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)