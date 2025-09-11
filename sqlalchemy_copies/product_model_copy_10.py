# This is copy #10 of product_model.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Optional

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
    
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    description: Optional[str] = Column(String(500))
    price: float = Column(Float, nullable=False)
    vendor_id: int = Column(Integer, ForeignKey('vendors.id'))
    
    # Relationships
    vendor: "Vendor" = relationship("Vendor", back_populates="products")
    categories: List["Category"] = relationship("Category", secondary=product_category, back_populates="products")
    reviews: List["Review"] = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Product(name='{self.name}', price={self.price})>"

class Vendor(Base):
    __tablename__ = 'vendors'
    
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100), nullable=False)
    
    # Relationships
    products: List["Product"] = relationship("Product", back_populates="vendor")

class Category(Base):
    __tablename__ = 'categories'
    
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(50), nullable=False)
    
    # Relationships
    products: List["Product"] = relationship("Product", secondary=product_category, back_populates="categories")

class Review(Base):
    __tablename__ = 'reviews'
    
    id: int = Column(Integer, primary_key=True)
    content: str = Column(String(500), nullable=False)
    rating: int = Column(Integer, nullable=False)
    product_id: int = Column(Integer, ForeignKey('products.id'))
    
    # Relationships
    product: "Product" = relationship("Product", back_populates="reviews")