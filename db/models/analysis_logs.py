from .base import Base
from sqlalchemy import Column , Integer  , Text , DateTime ,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class AnalysisLogs(Base):
    __tablename__ = "AnalysisLogs"
    
    id = Column(Integer , primary_key=True , index=True)
    input_data = Column(Text)
    output_data = Column(Text)
    createdAt = Column(DateTime , default= datetime.utcnow)
    
    user_id = Column(Integer , ForeignKey("users.id"))
    
    user = relationship("User" , back_populates='analysis_logs')