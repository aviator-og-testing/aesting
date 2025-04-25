# This is copy #3 of migration_script.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic
revision = 'a1b2c3d4e5f6'
down_revision = '1a2b3c4d5e6f'
branch_labels = None
depends_on = None

def upgrade():
    # Create new table
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add new column to existing table
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    
    # Create index
    op.create_index(op.f('ix_order_items_order_id'), 'order_items', ['order_id'], unique=False)
    
    # Insert data
    orders = table('orders',
        column('id', sa.Integer),
        column('status', sa.String)
    )
    
    op.bulk_insert(orders, [
        {'id': 1, 'status': 'pending'},
        {'id': 2, 'status': 'completed'},
    ])

def downgrade():
    # Drop index
    op.drop_index(op.f('ix_order_items_order_id'), table_name='order_items')
    
    # Drop column
    op.drop_column('users', 'phone')
    
    # Drop table
    op.drop_table('order_items')
