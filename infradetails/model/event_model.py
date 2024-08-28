from sqlalchemy import String,BigInteger,Column,Date
from infradetails.model.base_mixin_model import BaseMixinModel,Base

class EventModel(Base,BaseMixinModel):

    __tablename__ = "event"
    __table_args__ = {'schema':'event_management'}

    id = Column(BigInteger,primary_key=True,autoincrement=True,index=True)
    name = Column(String,nullable=False)
    start_date = Column(Date,nullable=False)
    end_date = Column(Date,nullable=False)
    status = Column(String,nullable=False)
