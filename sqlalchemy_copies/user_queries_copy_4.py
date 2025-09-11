# This is copy #4 of user_queries.py
from sqlalchemy import or_, and_, func, select
from sqlalchemy.orm import aliased
from db_session import Session
from user_model import User

def get_user_by_id(user_id):
    return Session().execute(select(User).where(User.id == user_id)).scalars().first()

def search_users(search_term):
    return Session().execute(select(User).where(
        or_(
            User.username.ilike(f'%{search_term}%'),
            User.email.ilike(f'%{search_term}%')
        )
    )).scalars().all()

def get_active_users():
    return Session().execute(select(User).where(User.is_active == True)).scalars().all()

def count_users():
    return Session().scalar(select(func.count(User.id)))

def update_user_status(user_id, is_active):
    session = Session()
    user = session.get(User, user_id)
    if user:
        user.is_active = is_active
        session.commit()
        return True
    return False