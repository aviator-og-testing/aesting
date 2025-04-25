# This is copy #9 of core_example.py
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, 
    Float, ForeignKey, select, join, func
)

# Create engine and metadata
engine = create_engine('postgresql://username:password@localhost:5432/mydatabase')
metadata = MetaData()

# Define tables
users = Table(
    'users', 
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('email', String(100), nullable=False)
)

orders = Table(
    'orders', 
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('total', Float, nullable=False),
    Column('status', String(20), nullable=False)
)

def create_tables():
    # Create tables in database
    metadata.create_all(engine)

def insert_data():
    # Insert data example
    with engine.connect() as conn:
        # Insert user
        ins_user = users.insert().values(
            name='John Doe',
            email='john@example.com'
        )
        result = conn.execute(ins_user)
        user_id = result.inserted_primary_key[0]
        
        # Insert orders
        ins_orders = orders.insert().values([
            {'user_id': user_id, 'total': 25.50, 'status': 'completed'},
            {'user_id': user_id, 'total': 30.00, 'status': 'pending'}
        ])
        conn.execute(ins_orders)

def query_data():
    # Select data example
    with engine.connect() as conn:
        # Simple select
        s = select(users).where(users.c.name == 'John Doe')
        result = conn.execute(s)
        for row in result:
            print(f"User: {row.name}, Email: {row.email}")
        
        # Join example
        j = select(
            users.c.name,
            orders.c.total,
            orders.c.status
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id)
        ).where(
            orders.c.total > 20
        )
        result = conn.execute(j)
        for row in result:
            print(f"User: {row.name}, Total: {row.total}, Status: {row.status}")
        
        # Aggregation
        s = select(
            users.c.name,
            func.count(orders.c.id).label('order_count'),
            func.sum(orders.c.total).label('total_spent')
        ).select_from(
            users.join(orders, users.c.id == orders.c.user_id)
        ).group_by(
            users.c.id, users.c.name
        )
        result = conn.execute(s)
        for row in result:
            print(f"User: {row.name}, Orders: {row.order_count}, Total: ${row.total_spent:.2f}")
