# This is copy #5 of product_model.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Many-to-many relationship table
product_category = Table(
    'product_category', 
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    
    # Relationships
    vendor = relationship("Vendor", back_populates="products")
    categories = relationship("Category", secondary=product_category, back_populates="products")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"

class Vendor(Base):
    __tablename__ = 'vendors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="vendor")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
    # Relationships
    products = relationship("Product", secondary=product_category, back_populates="categories")

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'))
    
    # Relationships
    product = relationship("Product", back_populates="reviews")
