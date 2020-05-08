import os
import re

from conf.db_conf import Session, engine, Base
from models.customer_product_model import Customer, Product, association_table
from models.product_type_model import ProductType
from models.payment_method_model import PaymentMethod

Base.metadata.create_all(engine)

session = Session()


def create_table(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def read_product_types(file_path):
    with open(file_path, 'r+') as file:
        buffer = file.read()
        first = re.split(r'PRODUCT_TYPES\n', buffer)[1]
        sec = re.split(r'.*\nPRODUCTS\n', first)[0]
        product_types = sec.split('\n')
        for i in range(0, len(product_types)):
            if product_types[i] != '':
                create_table(session, ProductType, id=i + 1, product_type=product_types[i])


def read_products(file_path):
    with open(file_path, 'r+') as file:
        buffer = file.read()
        first = re.split(r'PRODUCTS\n', buffer)[1]
        sec = re.split(r'.*\nPAYMENT METHODS\n', first)[0]
        products = sec.split('\n')
        for i in range(0, len(products)):
            values = products[i].split(',')
            print(values)
            if products[i] != '':
                create_table(session, Product, id=i + 1, product_name=values[0], price=values[1],
                             rating=values[2], type_id=values[3])


def read_payments(file_path):
    with open(file_path, 'r+') as file:
        buffer = file.read()
        first = re.split(r'PAYMENT METHODS\n', buffer)[1]
        sec = re.split(r'.*\nCUSTOMERS\n', first)[0]
        payments = sec.split('\n')
        for i in range(0, len(payments)):
            values = payments[i].split(',')
            print(values)
            if payments[i] != '':
                create_table(session, PaymentMethod, id=i + 1, card_number=values[0], paid_service=values[1],
                             customer_id=values[2])


def read_customers(file_path):
    with open(file_path, 'r+') as file:
        buffer = file.read()
        first = re.split(r'CUSTOMERS\n', buffer)[1]
        sec = re.split(r'.*\nCUSTOMER HAS PRODUCT\n', first)[0]
        customers = sec.split('\n')
        for i in range(0, len(customers)):
            values = customers[i].split(',')
            print(values)
            if customers[i] != '':
                create_table(session, Customer, id=i + 1, name=values[0], email=values[1])


def read_associations(file_path):
    with open(file_path, 'r+') as file:
        buffer = file.read()
        first = re.split(r'CUSTOMER HAS PRODUCT\n', buffer)[1]
        cust_product = first.split('\n')
        for i in range(0, len(cust_product)):
            values = cust_product[i].split(',')
            print(values)
            if cust_product[i] != '':
                insert_stmnt = association_table.insert().values(id_customer=values[0], id_product=values[1])
                session.execute(insert_stmnt)

                session.commit()


def create_db():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'data.csv')

    read_product_types(file_path)
    read_products(file_path)
    read_customers(file_path)
    read_payments(file_path)
    read_associations(file_path)


if __name__ == "__main__":
    create_db()
