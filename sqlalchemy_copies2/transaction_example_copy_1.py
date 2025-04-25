# This is copy #1 of transaction_example.py
from sqlalchemy.exc import IntegrityError
from db_session import Session
from user_model import User
from product_model import Product, Review

def create_product_with_reviews(product_data, reviews_data):
    """
    Create a product and its reviews in a single transaction
    """
    session = Session()
    try:
        # Start transaction
        new_product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            vendor_id=product_data['vendor_id']
        )
        session.add(new_product)
        session.flush()  # Flush to get the product ID
        
        # Add reviews
        for review_data in reviews_data:
            new_review = Review(
                content=review_data['content'],
                rating=review_data['rating'],
                product_id=new_product.id
            )
            session.add(new_review)
            
        # Commit the transaction
        session.commit()
        return new_product.id
    except IntegrityError as e:
        # Rollback in case of error
        session.rollback()
        raise e
    finally:
        session.close()

def transfer_products_between_vendors(old_vendor_id, new_vendor_id):
    """
    Transfer all products from one vendor to another in a transaction
    """
    session = Session()
    try:
        # Start transaction
        products = session.query(Product).filter(Product.vendor_id == old_vendor_id).all()
        
        for product in products:
            product.vendor_id = new_vendor_id
            
        session.commit()
        return len(products)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
