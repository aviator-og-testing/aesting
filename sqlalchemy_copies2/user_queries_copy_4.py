# This is copy #4 of user_queries.py
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import aliased
from db_session import Session
from user_model import User

def get_user_by_id(user_id):
    return Session().query(User).filter(User.id == user_id).first()

def search_users(search_term):
    return Session().query(User).filter(
        or_(
            User.username.ilike(f'%{search_term}%'),
            User.email.ilike(f'%{search_term}%')
        )
    ).all()

def get_active_users():
    return Session().query(User).filter(User.is_active == True).all()

def count_users():
    return Session().query(func.count(User.id)).scalar()

def update_user_status(user_id, is_active):
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.is_active = is_active
        session.commit()
        return True
    return False
