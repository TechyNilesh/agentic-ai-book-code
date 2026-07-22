"""Chapter 13 - Lab 13.1 setup helper (not printed in the book).

The book's lab says: "Create shop.db with tables customers(id, name)
and orders(id, customer_id, amount, ordered_at). Seed 20 customers and
200 orders." This script does exactly that minimal setup so
05_sqlite_server.py has data to query. Run it once before the lab.

Run:
    python 06_seed_db.py
"""
import random
import sqlite3
from datetime import datetime, timedelta

DB = "shop.db"


def seed():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS customers")
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("""CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        amount REAL,
        ordered_at TEXT
    )""")

    names = [f"Customer {i}" for i in range(1, 21)]
    cur.executemany("INSERT INTO customers (id, name) VALUES (?, ?)",
                     [(i + 1, name) for i, name in enumerate(names)])

    rng = random.Random(42)
    today = datetime(2026, 7, 23)
    orders = []
    for i in range(1, 201):
        customer_id = rng.randint(1, 20)
        amount = round(rng.uniform(100, 5000), 2)
        days_ago = rng.randint(0, 90)
        ordered_at = (today - timedelta(days=days_ago)).isoformat()
        orders.append((i, customer_id, amount, ordered_at))
    cur.executemany(
        "INSERT INTO orders (id, customer_id, amount, ordered_at) "
        "VALUES (?, ?, ?, ?)", orders)

    conn.commit()
    conn.close()
    print(f"Seeded {DB} with 20 customers and 200 orders.")


if __name__ == "__main__":
    seed()
