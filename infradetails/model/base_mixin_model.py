from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseMixinModel:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=True, default=None)
    updated_by = Column(String, nullable=True, default=None)
    is_active = Column(Boolean, default=False, nullable=False)
