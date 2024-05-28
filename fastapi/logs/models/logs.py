from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, DateTime, func
from sqlalchemy.orm import relationship
from database import Base  # Import Base from database module

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    level = Column(Enum('INFO', 'WARNING', 'ERROR', 'CRITICAL', name='log_levels'))
    user_id = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'level': self.level,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }