import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                              (id INTEGER PRIMARY KEY, name TEXT, price REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cart 
                              (user_id INTEGER, product_id INTEGER, quantity INTEGER)''')
        self.conn.commit()

    def add_product(self, name, price):
        self.cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute("SELECT * FROM products")
        return self.cursor.fetchall()

    def add_to_cart(self, user_id, product_id, quantity):
        self.cursor.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                            (user_id, product_id, quantity))
        self.conn.commit()

    def get_cart(self, user_id):
        self.cursor.execute(
            "SELECT products.name, products.price, cart.quantity FROM cart INNER JOIN products ON cart.product_id = products.id WHERE cart.user_id = ?",
            (user_id,))
        return self.cursor.fetchall()
