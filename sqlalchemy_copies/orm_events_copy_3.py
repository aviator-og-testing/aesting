# This is copy #3 of orm_events.py
from sqlalchemy import event, DDL
from sqlalchemy.orm import mapper
from db_session import engine, Base
from user_model import User
from product_model import Product

# Event listeners for User class
@event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, target):
    print(f"About to insert user: {target.username}")
    # Could perform validation or transformation here
    if target.username:
        target.username = target.username.lower()

@event.listens_for(User, 'after_insert')
def user_after_insert(mapper, connection, target):
    print(f"User inserted with ID: {target.id}")
    # Could send welcome email or perform other actions

# Event listeners for Product class
@event.listens_for(Product, 'before_update')
def product_before_update(mapper, connection, target):
    print(f"About to update product: {target.name}")
    # Validate price
    if target.price < 0:
        raise ValueError("Product price cannot be negative")

# DDL event - create an index after the table is created
event.listen(
    User.__table__, 
    'after_create',
    DDL("CREATE INDEX idx_user_email ON users (email)")
)

# Execute this function to setup all events
def setup_events():
    print("All ORM events have been set up")
