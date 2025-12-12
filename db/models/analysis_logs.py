from .base import Base
from sqlalchemy import Column , Integer, String , Text ,Float ,DateTime ,ForeignKey , CheckConstraint
from sqlalchemy.orm import relationship , validates
from datetime import datetime


class AnalysisLogs(Base):
    __tablename__ = "AnalysisLogs"
    
    id = Column(Integer , primary_key=True , index=True)
    text = Column(Text , nullable=False)
    score = Column(Float)
    category = Column(String)
    ton = Column(String)
    resume = Column(Text)
    createdAt = Column(DateTime , default= datetime.utcnow)
    user_id = Column(Integer , ForeignKey("users.id"))
    
    user = relationship("User" , back_populates='analysis_logs')
    
   