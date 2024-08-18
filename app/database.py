import sqlite3 as sq

db = sq.connect('products.db')
cur = db.cursor()

async def db_start():
    cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            cart_id TEXT)
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                description TEXT,
                price TEXT,
                photo TEXT,
                gender TEXT,
                brand TEXT,
                category TEXT
            )
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS brand(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_brand TEXT UNIQUE)
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS category(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_category TEXT UNIQUE)
        """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            status VARCHAR(10) DEFAULT 'pending')
    """)
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM users WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO users (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()

async def add_product(title,desc,price,photo,gender,brand,category):
    try:
        cur.execute("""
                INSERT INTO products (title, description, price, photo, gender, brand, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, desc, price, photo, gender, brand, category))
        db.commit()
        print("Product added successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def add_brand(branduser):
    try:
        cur.execute("INSERT INTO brand (name_brand) VALUES (?)", (branduser, ))
        db.commit()
        print(f"Brand {branduser} added successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def add_category(categoryprompt):
    try:
        cur.execute("INSERT INTO category (name_category) VALUES (?)", (categoryprompt, ))
        db.commit()
        print(f"Category {categoryprompt} added successfully")
    except Exception as e:
        print(f"An error occurred: {e}")


async def get_all_products():
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return products

async def get_all_user_ids():
    cur.execute("SELECT tg_id FROM users")
    users = cur.fetchall()
    return users


async def get_all_categories():
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    return categories

async def get_all_brands():
    cur.execute("SELECT * FROM brand")
    brands = cur.fetchall()
    return brands

async def get_all_tickets():
    cur.execute("SELECT * FROM tickets")
    tickets = cur.fetchall()
    return tickets

async def get_ticket_by_id(ticket_id):
    cur.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    tickets = cur.fetchone()
    return tickets
async def delete_ticket_by_id(ticket_id):
    try:
        cur.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

async def get_product_by_id(product_id):
    cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = cur.fetchone()
    return product

async def filter_product(gender, brand, category):
    products = await get_all_products()
    product_filtered = []

    for product in products:
        if gender == product[5] and brand == product[6] and category == product[7]:
                    product_filtered.append(product)
    if len(product_filtered) == 0:
        return "Таких товаров не найдено"
    else:
        return product_filtered


async def delete_product_by_id(product_id):
    try:
        cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        db.commit()
        print(f"Product {product_id} deleted successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def delete_brand_by_id(brand_id):
    try:
        cur.execute("DELETE FROM brand WHERE id=?", (brand_id,))
        db.commit()
        print(f"Product {brand_id} deleted successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def delete_category_by_id(catid):
    try:
        cur.execute("DELETE FROM category WHERE id=?", (catid,))
        db.commit()
        print(f"Product {catid} deleted successfully")
    except Exception as e:
        print(f"An error occurred: {e}")

async def create_user_ticket(userid,text):
    try:
        cur.execute("""
                        INSERT INTO tickets(user_id, text)
                        VALUES (?, ?)
                    """, (userid,text))
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")