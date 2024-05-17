from sqlalchemy import Column, Integer, String, ForeignKey, Table, Enum, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from database import Base  # Import Base from database module

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tasks = relationship('Task', back_populates='user')

    def to_dict(self):
        """Return dictionary representation of the User."""
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at.isoformat() if self.created_at else None,  # Format datetime as string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "tasks": [task.to_dict() for task in self.tasks]
        }

