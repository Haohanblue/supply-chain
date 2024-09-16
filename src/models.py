# models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255))

class City(Base):
    __tablename__ = 'Cities'
    city_id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String(255))

class Month(Base):
    __tablename__ = 'Months'
    month_id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer)

class Stock(Base):
    __tablename__ = 'Stock'
    stock_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    month_id = Column(Integer, ForeignKey('Months.month_id'))
    city_id = Column(Integer, ForeignKey('Cities.city_id'))
    product_id = Column(Integer, ForeignKey('Products.product_id'))
    quantity = Column(Integer)

    # 禁用自动加载关联对象
    city = relationship('City', lazy='noload')
    product = relationship('Product', lazy='noload')
    month = relationship('Month', lazy='noload')
