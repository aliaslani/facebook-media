# create_fake_posts.py

import os
import random
import django
from faker import Faker
import faker_commerce

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook.settings')
django.setup()


from market.models import Sales, Client, Product


fake = Faker()
fake.add_provider(faker_commerce.Provider)
NUMBER_OF_CLIENTS = 50
NUMBER_OF_SALES = 10000
NUMBER_OF_PRODUCTS = 100

skues = [
    'SP',  # sport
    'MU',  # music
    'MO',  # movie
    'TE',  # tech
]

clients = []
products = []
sales = []
for _ in range(NUMBER_OF_CLIENTS):

    client = Client.objects.create(
        name = fake.name(),
        country = fake.country(),
    )
    clients.append(client)
for _ in range(NUMBER_OF_PRODUCTS):
    product = Product.objects.create(
    name = fake.ecommerce_name(),
    sku = random.choice(skues),
    )
    products.append(product)




for _ in range(NUMBER_OF_SALES):

    sales = Sales.objects.create(
            client = random.choice(clients),
            product = random.choice(products),
            doc_date = fake.date(),
            quantity = random.randint(1, 100),
            price = random.randint(1, 1000),
            value = random.randint(1, 100),
        )


print('\nFake data created successfully!')