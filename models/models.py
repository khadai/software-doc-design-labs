from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from conf.db_conf import Base, session


def check_required_fields_in_dict(fields, dictionary):
    error = []
    for field in fields:
        if field not in dictionary:
            error.append("Field: {field} not in input data".format(field=field))
        else:
            print(field)
            print(dictionary["product_name"])

            continue

    if len(error) <= 0:
        return True, []
    else:
        return False, error


class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column(Integer, primary_key=True)
    product_type = Column(String)

    def __repr__(self):
        return "<Product_type: {}>".format(self.product_type)


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

    def __repr__(self):
        return "<Customer name: {}, email: {}>".format(self.name, self.email)


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

    @staticmethod
    def required_fields_list():
        return ["product_name", "price", "rating", "type"]

    @staticmethod
    def load_from_dict(data):
        check, errors = check_required_fields_in_dict(Product.required_fields_list(), data)
        print('here1'+str(check))
        if check:
            session.add(Product(product_name=data["product_name"], type_id=data['type'], price=data['price'], rating=0))
            session.commit()
        else:
            raise Exception(errors)

    def edit(self, info):
        self.product_name = info["product_name"]
        self.price = float(info["price"])
        self.rating = float(info["rating"])

        print(info)
        p_type = session.query(ProductType).get(self.type_id)
        p_type.product_type = info["product_type"]
        session.commit()

    def remove(self):
        session.delete(self)
        session.commit()

    def serialize(self, includes=[]):
        p_type = session.query(ProductType).get(self.type_id)

        return {
            'id': self.id,
            'product_name': self.product_name,
            'price': self.price,
            'rating': self.rating,
            'product_type': p_type.product_type
        }


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    paid_service = Column(String)
    customer_id = Column(Integer, ForeignKey(Customer.id))
    customer = relationship(Customer)

    def __repr__(self):
        return "<Card number: {}, paid service: {}>".format(self.card_number, self.paid_service)
