


from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,BigInteger
from infradetails.model.base_mixin_model import Base, BaseMixinModel
from infradetails.model.event_model import EventModel
from infradetails.model.user_model import UserModel
class EventSubscriberModel(Base,BaseMixinModel):

    __tablename__ = 'event_subscriber'
    __table_args__ = {'schema': 'event_management'}

    id = Column(BigInteger,primary_key=True,index=True,autoincrement=True)
    user_id = Column(BigInteger,ForeignKey(UserModel.id),nullable=False)
    event_id = Column(BigInteger,ForeignKey(EventModel.id),nullable=False)
    status = Column(String,nullable=False)



