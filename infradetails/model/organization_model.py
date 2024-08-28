
from sqlalchemy import Column, Integer, String, Boolean,BigInteger
from sqlalchemy.orm import relationship
from infradetails.model.base_mixin_model import Base, BaseMixinModel


class OrganizationModel(Base, BaseMixinModel):
    __tablename__ = 'organization'
    __table_args__ = {'schema': 'event_management'}

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
