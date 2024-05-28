import os

import psycopg2
from contextlib import contextmanager
from dotenv import load_dotenv,dotenv_values
load_dotenv()
@contextmanager
def ConnectDb():
    try:
        database =os.getenv('database')
        password = os.getenv('password')
        host = os.getenv('host')
        port = os.getenv('port')
        user = os.getenv('user')

        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        yield conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        yield None

class Product:
    def __init__(self, title, price):
        self.title = title
        self.price = price

# Example usage:
with ConnectDb() as db_conn:
    if db_conn:
        product = Product(title="Motorola", price=200)

        with db_conn.cursor() as cursor:
            cursor.execute("INSERT INTO products (title, price) VALUES (%s, %s)", (product.title, product.price))
            db_conn.commit()
        print("Product inserted successfully!")
    else:
        print("Failed to connect to the database.")
