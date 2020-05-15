import random
import names


class CsvGenerator:
    file_name = 'data.csv'

    PRODUCTS_AMOUNT = 300
    CUST_HAS_PRODUCTS_AMOUNT = 200
    CUSTOMERS_AMOUNT = 300
    PAYMENT_METHODS_AMOUNT = 200

    products_types = ['Book', 'Film', 'Music', 'App']
    paid_services = ['Visa', 'MasterCard', 'American Express']
    emails = ['gmail.com', 'ukr.net']

    def generate_types(self, file):
        file.write('\nPRODUCT_TYPES\n')
        for i in self.products_types:
            file.write('{type_name}\n'.format(type_name=i))

    def generate_products(self, file, amount):
        file.write('\nPRODUCTS\n')
        for i in range(0, amount):
            product_name = names.get_last_name()
            price = round(random.uniform(0.0, 100.0), 2)
            rating = round(random.uniform(1.0, 5.0), 1)
            id_type = random.randint(1, 4)
            file.write('{product_name},{price},{rating},{id_type}\n'.format(product_name=product_name,
                                                                            price=price,
                                                                            rating=rating,
                                                                            id_type=id_type))

    def generate_payments(self, file, amount):
        file.write('\nPAYMENT METHODS\n')
        for i in range(0, amount):
            card_number = random.randrange(1000000000000000, 9999999999999999)
            paid_service = random.choice(self.paid_services)
            id_customer = random.randint(1, self.CUSTOMERS_AMOUNT)
            file.write('{card_number},{paid_service},{id_customer}\n'.format(card_number=card_number,
                                                                             paid_service=paid_service,
                                                                             id_customer=id_customer))

    def generate_cust_has_product(self, file, amount):
        file.write('\nCUSTOMER HAS PRODUCT\n')
        for i in range(0, amount):
            id_product = random.randint(1, self.PRODUCTS_AMOUNT)
            id_customer = random.randint(1, self.CUSTOMERS_AMOUNT)
            file.write('{},{}\n'.format(id_customer, id_product))

    def generate_customers(self, file, amount):
        file.write('\nCUSTOMERS\n')
        for i in range(0, amount):
            last_name_cust = names.get_last_name()
            first_name_cust = names.get_first_name()
            name_customer = '{} {}'.format(first_name_cust, last_name_cust)
            email = '{}.{}@{}'.format(first_name_cust, last_name_cust, random.choice(self.emails)).lower()
            random.choice(self.paid_services)
            file.write('{name_customer},{email}\n'.format(name_customer=name_customer,
                                                          email=email))

    def generate_csv(self):
        with open(self.file_name, 'w') as file:
            self.generate_types(file)
            self.generate_products(file, self.PRODUCTS_AMOUNT)
            self.generate_payments(file, self.PAYMENT_METHODS_AMOUNT)
            self.generate_customers(file, self.CUSTOMERS_AMOUNT)
            self.generate_cust_has_product(file, self.CUST_HAS_PRODUCTS_AMOUNT)
            print("CSV generated!")


if __name__ == '__main__':
    csv_gen = CsvGenerator()
    csv_gen.generate_csv()
