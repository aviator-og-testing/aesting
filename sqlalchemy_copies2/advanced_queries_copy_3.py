# This is copy #3 of advanced_queries.py
from sqlalchemy import func, desc, case, text, select
from sqlalchemy.orm import aliased
from db_session import Session
from user_model import User
from product_model import Product, Category, Review

def get_product_with_reviews():
    session = Session()
    stmt = select(
        Product,
        func.count(Review.id).label('review_count'),
        func.avg(Review.rating).label('avg_rating')
    ).join(
        Review, Product.id == Review.product_id, isouter=True
    ).group_by(
        Product.id
    ).having(
        func.count(Review.id) > 0
    ).order_by(
        desc('avg_rating')
    )

def get_product_by_category(category_name):
    session = Session()
    stmt = select(Product) \
        .join(Product.categories) \
        .where(Category.name == category_name)
    return session.execute(stmt).scalars().all()

def get_top_rated_products(limit=5):
    session = Session()
    stmt = select(
        Product.id,
        Product.name,
        func.avg(Review.rating).label('average_rating')
    ).join(
        Review, Product.id == Review.product_id
    ).group_by(
        Product.id, Product.name
    ).order_by(
        desc('average_rating')
    ).limit(limit)

def get_products_with_price_range(min_price, max_price):
    session = Session()
    stmt = select(Product) \
        .where(Product.price >= min_price, Product.price <= max_price) \
        .order_by(Product.price)
    return session.execute(stmt).scalars().all()