

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,BigInteger
from sqlalchemy.orm import relationship
from infradetails.model.base_mixin_model import Base, BaseMixinModel
from infradetails.model.organization_model import OrganizationModel


class OfficeModel(Base, BaseMixinModel):
    __tablename__ = 'office'
    __table_args__ = {'schema': 'event_management'}

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_deleted = Column(Boolean, nullable=True)
    org_id = Column(BigInteger, ForeignKey(OrganizationModel.id), nullable=False)


