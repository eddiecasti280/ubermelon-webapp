#!/usr/bin/env python3
"""
Data model for the Food Shop application.

This module provides classes and functions to interact with the SQLite database.
It includes the Item class for food products and Customer class for users.
"""

import sqlite3
import hashlib
from typing import Optional, List


class Item:
    """
    A wrapper object that corresponds to rows in the items table.
    
    Attributes:
        id: Unique identifier for the item.
        category: Category of the food item (e.g., 'Fruit', 'Vegetable').
        name: Display name of the item.
        price: Price of the item in dollars.
        imgurl: URL path to the item's image.
        description: Detailed description of the item.
        in_stock: Boolean indicating if item is available.
        stock_count: Number of units currently in stock.
    """
    
    def __init__(self, id: int, category: str, name: str, price: float, 
                 imgurl: str, description: str, in_stock: bool = True,
                 stock_count: int = 0):
        self.id = id
        self.category = category
        self.name = name
        self.price = price
        self.imgurl = imgurl
        self.description = description
        self.in_stock = bool(in_stock)
        self.stock_count = stock_count

    def price_str(self) -> str:
        """Return the price formatted as a currency string."""
        return f"${self.price:.2f}"

    def stock_value(self) -> float:
        """Return total value of this item's stock."""
        return self.price * self.stock_count

    def stock_value_str(self) -> str:
        """Return formatted total value of this item's stock."""
        return f"${self.stock_value():.2f}"

    def __repr__(self) -> str:
        return f"<Item: {self.id}, {self.name}, {self.price_str()}>"


class Customer:
    """
    A wrapper object corresponding to one customer in the database.
    
    Attributes:
        id: Unique identifier.
        email: Customer's email address (unique identifier).
        name: Customer's display name.
        role: 'user' or 'admin'.
    """
    
    def __init__(self, id: int, email: str, name: str, role: str = "user"):
        self.id = id
        self.email = email
        self.name = name
        self.role = role

    def is_admin(self) -> bool:
        """Return True if this customer has admin privileges."""
        return self.role == "admin"

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email
    
    def __repr__(self) -> str:
        return f"<Customer: {self.name}, {self.email}, role={self.role}>"


def hash_password(password: str) -> str:
    """
    Hash a password using SHA-256.
    
    Note: In production use bcrypt or argon2 instead.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def connect():
    """
    Establish a connection to the SQLite database.
    
    Returns:
        tuple: (connection, cursor) so callers can commit if needed.
    """
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()
    return conn, cursor


def get_items() -> List[Item]:
    """
    Query the database for all available items.
    """
    conn, cursor = connect()
    query = """SELECT id, category, name, price, imgurl,
                      description, in_stock, stock_count
               FROM items
               WHERE imgurl <> ''
               ORDER BY category, name
               LIMIT 50;"""

    cursor.execute(query)
    item_rows = cursor.fetchall()
    conn.close()

    items = []
    for row in item_rows:
        item = Item(
            id=row[0], category=row[1], name=row[2], price=row[3],
            imgurl=row[4], description=row[5], in_stock=row[6],
            stock_count=row[7]
        )
        items.append(item)

    print(f"Retrieved {len(items)} items from database")
    return items


def get_item_by_id(id: int) -> Optional[Item]:
    """
    Query for a specific item in the database by primary key.
    """
    conn, cursor = connect()
    query = """SELECT id, category, name, price, imgurl,
                      description, in_stock, stock_count
               FROM items
               WHERE id = ?;"""

    cursor.execute(query, (id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None

    return Item(
        id=row[0], category=row[1], name=row[2], price=row[3],
        imgurl=row[4], description=row[5], in_stock=row[6],
        stock_count=row[7]
    )


def get_items_by_category(category: str) -> List[Item]:
    """
    Query for all items in a specific category.
    """
    conn, cursor = connect()
    query = """SELECT id, category, name, price, imgurl,
                      description, in_stock, stock_count
               FROM items
               WHERE category = ?
               ORDER BY name;"""

    cursor.execute(query, (category,))
    item_rows = cursor.fetchall()
    conn.close()

    items = []
    for row in item_rows:
        item = Item(
            id=row[0], category=row[1], name=row[2], price=row[3],
            imgurl=row[4], description=row[5], in_stock=row[6],
            stock_count=row[7]
        )
        items.append(item)
    return items


def get_all_categories() -> List[str]:
    """Return a sorted list of all distinct categories."""
    conn, cursor = connect()
    cursor.execute("SELECT DISTINCT category FROM items ORDER BY category;")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_inventory_summary() -> dict:
    """
    Return a summary of the full inventory for admin dashboard.
    
    Returns dict with:
        total_items: number of distinct products
        total_stock: total units across all products
        total_value: total dollar value of all stock
        in_stock_count: number of products currently in stock
        out_of_stock_count: number of products out of stock
        categories: dict mapping category name to list of items
    """
    conn, cursor = connect()
    
    cursor.execute("""
        SELECT id, category, name, price, imgurl,
               description, in_stock, stock_count
        FROM items
        ORDER BY category, name;
    """)
    rows = cursor.fetchall()
    conn.close()

    items = []
    for row in rows:
        items.append(Item(
            id=row[0], category=row[1], name=row[2], price=row[3],
            imgurl=row[4], description=row[5], in_stock=row[6],
            stock_count=row[7]
        ))

    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)

    total_stock = sum(i.stock_count for i in items)
    total_value = sum(i.stock_value() for i in items)
    in_stock = sum(1 for i in items if i.in_stock)
    out_of_stock = sum(1 for i in items if not i.in_stock)

    return {
        "total_items": len(items),
        "total_stock": total_stock,
        "total_value": total_value,
        "in_stock_count": in_stock,
        "out_of_stock_count": out_of_stock,
        "categories": categories,
        "all_items": items,
    }


def update_item_stock(item_id: int, stock_count: int, in_stock: bool) -> bool:
    """
    Update the stock count and availability of an item.
    
    Returns True if the update succeeded.
    """
    conn, cursor = connect()
    try:
        cursor.execute(
            "UPDATE items SET stock_count = ?, in_stock = ? WHERE id = ?;",
            (stock_count, int(in_stock), item_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def update_item(item_id: int, name: str, price: float, category: str,
                description: str, stock_count: int, in_stock: bool) -> bool:
    """
    Update all editable fields of an item.
    
    Returns True if the update succeeded.
    """
    conn, cursor = connect()
    try:
        cursor.execute("""
            UPDATE items
            SET name = ?, price = ?, category = ?,
                description = ?, stock_count = ?, in_stock = ?
            WHERE id = ?;
        """, (name, price, category, description, stock_count, int(in_stock), item_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def authenticate_customer(email: str, password: str) -> Optional[Customer]:
    """
    Verify credentials and return a Customer if they match.
    
    Returns None if email not found or password incorrect.
    """
    conn, cursor = connect()
    query = """SELECT id, email, name, password_hash, role
               FROM customers
               WHERE email = ?;"""
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    stored_hash = row[3]
    if stored_hash != hash_password(password):
        return None

    return Customer(id=row[0], email=row[1], name=row[2], role=row[4])


def get_customer_by_email(email: str) -> Optional[Customer]:
    """
    Query for a customer by their email address.
    """
    conn, cursor = connect()
    query = """SELECT id, email, name, role
               FROM customers
               WHERE email = ?;"""
    cursor.execute(query, (email,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return Customer(id=row[0], email=row[1], name=row[2], role=row[3])