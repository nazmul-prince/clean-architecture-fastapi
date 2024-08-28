from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, ForeignKey

from infradetails.model.base_mixin_model import BaseMixinModel, Base
from infradetails.model.role_model import RoleModel
from infradetails.model.user_model import UserModel


class UserRoleModel(Base, BaseMixinModel):
    __tablename__ = "user_role"
    __table_args__ = {"schema": "event_management"}

    id = Column(Integer, primary_key=True, index=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(UserModel.id), nullable=False)
    role_id = Column(Integer, ForeignKey(RoleModel.id), nullable=False)