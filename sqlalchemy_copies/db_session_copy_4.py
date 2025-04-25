# This is copy #4 of db_session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Create engine
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Import all models to ensure they're registered
    from user_model import User
    from product_model import Product
    
    Base.metadata.create_all(bind=engine)
