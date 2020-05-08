from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.customer_product_model import Customer

from conf.db_conf import Base


class PaymentMethod(Base):
    __tablename__ = 'payment_method'

    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    paid_service = Column(String)
    customer_id = Column(Integer, ForeignKey(Customer.id))
    customer = relationship(Customer)

    def __init__(self, id, card_number, paid_service, customer_id):
        self.id = id
        self.card_number = card_number
        self.paid_service = paid_service
        self.customer_id = customer_id