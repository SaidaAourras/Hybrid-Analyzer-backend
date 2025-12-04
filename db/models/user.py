from .base import Base
from sqlalchemy import Column , Integer , String , Date 
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer , primary_key=True , index=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    createdAt = Column(Date , default= datetime.utcnow)
    
    analysis_log = relationship("Analysis_logs" , back_populates="owner")

    