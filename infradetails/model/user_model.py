from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, Nullable
from infradetails.model.base_mixin_model import Base, BaseMixinModel
from infradetails.model.office_model import OfficeModel
from sqlalchemy.orm import relationship


class UserModel(Base, BaseMixinModel):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'event_management'}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    office_id = Column(Integer,ForeignKey(OfficeModel.id), nullable=False)
    is_active = Column(Boolean,nullable=False)
