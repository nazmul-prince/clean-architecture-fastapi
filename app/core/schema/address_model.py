from sqlalchemy import Column, Integer, String

from infradetails.model.base_mixin_model import Base, BaseMixinModel


class AddressModel(Base, BaseMixinModel):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'core'}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    division = Column(String, unique=True, index=True, nullable=False)
    zilla = Column(String, nullable=False)
    upazilla = Column(String, nullable=False)
    municipality = Column(String, nullable=False)
    thana_union = Column(String, nullable=False)
    ward = Column(String, nullable=False)
    addr_ids = Column(String, nullable=False)
    addr_details = Column(String, nullable=False)
