# This is copy #4 of custom_types.py
import json
from sqlalchemy import TypeDecorator, Text
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func

Base = declarative_base()

# Custom JSON type
class JsonType(TypeDecorator):
    impl = Text
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

# SQLAlchemy will detect changes to dictionaries
MutableJsonDict = MutableDict.as_mutable(JsonType)

# Mixin class for timestamp columns
class TimestampMixin:
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

# Example model using custom type and mixin
class Configuration(TimestampMixin, Base):
    __tablename__ = 'configurations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    settings = Column(MutableJsonDict, nullable=False, default={})
    
    def __repr__(self):
        return f"<Configuration(name='{self.name}')>"

# Usage example
def save_configuration():
    from db_session import Session
    
    session = Session()
    config = Configuration(
        name="App Settings",
        settings={
            "theme": "dark",
            "notifications": True,
            "timeout": 300,
            "features": ["comments", "sharing", "export"]
        }
    )
    session.add(config)
    session.commit()
    
    # Update JSON directly
    config.settings["theme"] = "light"  # This change will be detected
    session.commit()
