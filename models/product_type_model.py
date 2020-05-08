from sqlalchemy import Column, String, Integer

from conf.db_conf import Base


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(Integer, primary_key=True)
    product_type = Column(String)

    def __init__(self, id, product_type):
        self.id = id
        self.product_type = product_type
