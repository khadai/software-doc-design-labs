from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from conf.db_conf import Base
from models.product_type_model import ProductType

association_table = Table('association', Base.metadata,
                          Column('id_customer', Integer, ForeignKey('customer.id')),
                          Column('id_product', Integer, ForeignKey('product.id'))
                          )


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    products = relationship(
        'Product',
        secondary=association_table,
        back_populates='customers')  # lazy='dynamic'

    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    type_id = Column(Integer, ForeignKey(ProductType.id))
    type = relationship(ProductType)
    customers = relationship(
        'Customer',
        secondary=association_table,
        back_populates='products')

    def __init__(self, id, product_name, type_id, price, rating):
        self.id = id
        self.product_name = product_name
        self.type_id = type_id
        self.price = price
        self.rating = rating
