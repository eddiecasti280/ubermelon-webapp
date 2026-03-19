#!/usr/bin/env python3
"""
Data model for the Food Shop application.

This module provides classes and functions to interact with the SQLite database.
It includes the Item class for food products and Customer class for users.
"""

import sqlite3
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
    """
    
    def __init__(self, id: int, category: str, name: str, price: float, 
                 imgurl: str, description: str, in_stock: bool = True):
        self.id = id
        self.category = category
        self.name = name
        self.price = price
        self.imgurl = imgurl
        self.description = description
        self.in_stock = bool(in_stock)

    def price_str(self) -> str:
        """Return the price formatted as a currency string."""
        return f"${self.price:.2f}"

    def __repr__(self) -> str:
        return f"<Item: {self.id}, {self.name}, {self.price_str()}>"


class Customer:
    """
    A wrapper object corresponding to one customer in the database.
    
    Attributes:
        email: Customer's email address (unique identifier).
        name: Customer's display name.
    """
    
    def __init__(self, email: str, name: str):
        self.email = email
        self.name = name

    def get_name(self) -> str:
        """Return the customer's name."""
        return self.name

    def get_email(self) -> str:
        """Return the customer's email."""
        return self.email
    
    def __repr__(self) -> str:
        return f"<Customer: {self.name}, {self.email}>"


def connect():
    """
    Establish a connection to the SQLite database.
    
    Returns:
        sqlite3.Cursor: A cursor object for executing queries.
    """
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()
    return cursor


def get_items() -> List[Item]:
    """
    Query the database for all available items.
    
    Returns:
        List[Item]: A list of Item objects representing all products.
    """
    cursor = connect()
    query = """SELECT id, category, name, price, imgurl, description, in_stock
               FROM items
               WHERE imgurl <> ''
               ORDER BY category, name
               LIMIT 50;"""

    cursor.execute(query)
    item_rows = cursor.fetchall()

    items = []
    for row in item_rows:
        item = Item(
            id=row[0],
            category=row[1],
            name=row[2],
            price=row[3],
            imgurl=row[4],
            description=row[5],
            in_stock=row[6]
        )
        items.append(item)

    print(f"Retrieved {len(items)} items from database")
    return items


def get_item_by_id(id: int) -> Optional[Item]:
    """
    Query for a specific item in the database by primary key.
    
    Args:
        id: The unique identifier of the item.
    
    Returns:
        Item or None: The Item object if found, None otherwise.
    """
    cursor = connect()
    query = """SELECT id, category, name, price, imgurl, description, in_stock
               FROM items
               WHERE id = ?;"""

    cursor.execute(query, (id,))
    row = cursor.fetchone()
    
    if not row:
        return None

    item = Item(
        id=row[0],
        category=row[1],
        name=row[2],
        price=row[3],
        imgurl=row[4],
        description=row[5],
        in_stock=row[6]
    )
    
    return item


def get_items_by_category(category: str) -> List[Item]:
    """
    Query for all items in a specific category.
    
    Args:
        category: The category name to filter by.
    
    Returns:
        List[Item]: A list of Item objects in the specified category.
    """
    cursor = connect()
    query = """SELECT id, category, name, price, imgurl, description, in_stock
               FROM items
               WHERE category = ?
               ORDER BY name;"""

    cursor.execute(query, (category,))
    item_rows = cursor.fetchall()

    items = []
    for row in item_rows:
        item = Item(
            id=row[0],
            category=row[1],
            name=row[2],
            price=row[3],
            imgurl=row[4],
            description=row[5],
            in_stock=row[6]
        )
        items.append(item)

    return items


def get_customer_by_email(email: str) -> Optional[Customer]:
    """
    Query for a customer by their email address.
    
    Args:
        email: The customer's email address.
    
    Returns:
        Customer or None: The Customer object if found, None otherwise.
    """
    cursor = connect()
    query = """SELECT name, email 
               FROM customers
               WHERE email = ?;"""
    cursor.execute(query, (email,))
    row = cursor.fetchone()

    if not row:
        return None

    customer = Customer(name=row[0], email=row[1])
    return customer