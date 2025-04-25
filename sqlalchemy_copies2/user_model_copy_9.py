# This is copy #9 of user_model.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
    password_hash: str = Column(String(128), nullable=False)
    is_active: bool = Column(Boolean, default=True)
    created_at: DateTime = Column(DateTime, default=func.now())
    updated_at: DateTime = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"