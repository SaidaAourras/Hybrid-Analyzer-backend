from .base import Base
from sqlalchemy import Column , Integer , String , Date , CheckConstraint
from datetime import datetime
from sqlalchemy.orm import relationship , validates
import re


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer , primary_key=True , index=True)
    username = Column(String , nullable=False , unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String , nullable=False)
    createdAt = Column(Date , default= datetime.utcnow)
    
    analysis_logs = relationship("AnalysisLogs" , back_populates="user")
    
    # __table_args__ = (
    #     CheckConstraint("length(username) >= 3", name="username_min_length"),
    #     CheckConstraint("length(email) >= 3", name="email_min_length"),
    # )

   
    