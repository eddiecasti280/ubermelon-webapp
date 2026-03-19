#!/usr/bin/env python3
"""
Database initialization script for Food Shop.

This script creates the SQLite database and populates it with food items,
customer accounts, and admin accounts for demo purposes.
"""

import sqlite3
import os
import hashlib


def hash_password(password):
    """
    Hash a password using SHA-256.
    
    Note: In a production application, use bcrypt or argon2 instead.
    This is simplified for demo purposes.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def init_database():
    """Initialize the database with tables and food item data."""
    
    # Remove existing database
    if os.path.exists("food.db"):
        os.remove("food.db")
        print("Removed existing database.")
    
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()
    
    # Create items table
    cursor.execute("""
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            imgurl TEXT NOT NULL,
            description TEXT,
            in_stock INTEGER DEFAULT 1,
            stock_count INTEGER DEFAULT 50
        );
    """)
    
    # Create customers table with role support
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );
    """)
    
    # Food item data based on the sprite sheet
    food_items = [
        # Apples (Category: Fruit)
        ("Fruit", "Red Apple", 0.99, "/static/img/sprites/red_apple.png",
         "A classic red apple, sweet and crispy. Perfect for snacking or baking.", 1, 120),
        ("Fruit", "Granny Smith Apple", 1.09, "/static/img/sprites/granny_smith_apple.png",
         "Tart and tangy green apple. Great for pies and salads.", 1, 85),
        ("Fruit", "Golden Delicious Apple", 1.19, "/static/img/sprites/golden_delicious_apple.png",
         "Sweet yellow apple with a mild flavor. Excellent eating apple.", 1, 64),
        ("Fruit", "Ambrosia Apple", 1.49, "/static/img/sprites/ambrosia_apple.png",
         "Sweet and aromatic apple with honey-like flavor notes.", 1, 40),
        ("Fruit", "Honeycrisp Apple", 1.79, "/static/img/sprites/honeycrisp_apple.png",
         "Exceptionally crisp and juicy with balanced sweet-tart flavor.", 1, 55),
        ("Fruit", "Half Apple", 0.59, "/static/img/sprites/half_apple.png",
         "Pre-cut apple half, perfect for quick snacks.", 1, 30),
        
        # Pears (Category: Fruit)
        ("Fruit", "Concorde Pear", 1.29, "/static/img/sprites/concorde_pear.png",
         "Sweet vanilla-flavored pear that doesn't brown quickly when cut.", 1, 45),
        ("Fruit", "Bartlett Pear", 1.19, "/static/img/sprites/bartlett_pear.png",
         "Classic pear with smooth, sweet flesh. Great for canning.", 1, 72),
        ("Fruit", "Bosk Pear", 1.39, "/static/img/sprites/bosk_pear.png",
         "Firm, dense pear with warm spice and honey undertones.", 1, 38),
        ("Fruit", "Chinese White Pear", 1.59, "/static/img/sprites/chinese_white_pear.png",
         "Crisp Asian pear with refreshing, light sweetness.", 1, 25),
        ("Fruit", "Forelle Pear", 1.49, "/static/img/sprites/forelle_pear.png",
         "Small, sweet pear with distinctive red freckling.", 1, 50),
        ("Fruit", "Seckel Pear", 0.99, "/static/img/sprites/seckel_pear.png",
         "Tiny 'sugar pear' with intense sweetness. Perfect bite-sized treat.", 1, 60),
        ("Fruit", "Conference Pear", 1.29, "/static/img/sprites/conference_pear.png",
         "Long, slender pear with sweet, slightly tangy flavor.", 1, 42),
        
        # Vegetables (Category: Vegetable)
        ("Vegetable", "Tomato", 0.79, "/static/img/sprites/tomato.png",
         "Ripe red tomato, perfect for salads, sandwiches, or cooking.", 1, 200),
        ("Vegetable", "Yellow Tomato", 0.89, "/static/img/sprites/yellow_tomato.png",
         "Milder, less acidic tomato variety with sunny color.", 1, 90),
        ("Vegetable", "Pumpkin", 4.99, "/static/img/sprites/pumpkin.png",
         "Perfect for pies, soups, or autumn decoration.", 1, 15),
        ("Vegetable", "Carrot", 0.49, "/static/img/sprites/carrot.png",
         "Fresh, crunchy carrot. Great raw or cooked.", 1, 300),
        ("Vegetable", "Pea Pod", 2.49, "/static/img/sprites/pea_pod.png",
         "Fresh snap peas in the pod. Sweet and crunchy.", 1, 80),
        ("Vegetable", "Bell Pepper", 1.29, "/static/img/sprites/bell_pepper.png",
         "Crisp red bell pepper, sweet and versatile.", 1, 110),
        ("Vegetable", "Yellow Bell Pepper", 1.29, "/static/img/sprites/yellow_bell_pepper.png",
         "Sweet yellow bell pepper, milder than green varieties.", 1, 95),
        ("Vegetable", "Green Bell Pepper", 0.99, "/static/img/sprites/green_bell_pepper.png",
         "Classic green bell pepper with slightly bitter, fresh taste.", 1, 130),
        
        # Breakfast/Fast Food (Category: Prepared Food)
        ("Prepared Food", "Scrambled Egg", 2.99, "/static/img/sprites/scrambled_egg.png",
         "Fluffy scrambled eggs, made fresh to order.", 1, 50),
        ("Prepared Food", "Bacon", 3.49, "/static/img/sprites/bacon.png",
         "Strips of perfectly cooked bacon.", 1, 75),
        ("Prepared Food", "Crispy Bacon", 3.99, "/static/img/sprites/crispy_bacon.png",
         "Extra crispy bacon for those who like it crunchy.", 1, 60),
        ("Prepared Food", "Cheese", 2.99, "/static/img/sprites/cheese.png",
         "Slice of quality cheese, perfect for sandwiches.", 1, 100),
        ("Prepared Food", "Pizza Slice", 3.49, "/static/img/sprites/pizza_slice.png",
         "Hot slice of pepperoni pizza.", 1, 45),
        ("Prepared Food", "Hot Dog", 2.99, "/static/img/sprites/hot_dog.png",
         "Classic hot dog with all the fixings.", 0, 0),
        
        # Holiday Treats (Category: Holiday)
        ("Holiday", "Candy Cane", 0.99, "/static/img/sprites/candy_cane.png",
         "Traditional peppermint candy cane. Festive and sweet!", 1, 200),
        ("Holiday", "Gingerbread Man", 2.49, "/static/img/sprites/gingerbread_man.png",
         "Decorated gingerbread cookie shaped like a person.", 1, 35),
        ("Holiday", "Gingerbread Man Base", 1.99, "/static/img/sprites/gingerbread_man_base.png",
         "Undecorated gingerbread cookie - decorate it yourself!", 1, 40),
        ("Holiday", "Gingerbread House", 12.99, "/static/img/sprites/gingerbread_house.png",
         "Beautiful edible gingerbread house kit.", 1, 10),
        ("Holiday", "Glühwein", 4.99, "/static/img/sprites/glintwein.png",
         "Traditional mulled wine with warm spices.", 1, 20),
        ("Holiday", "Eggnog", 3.99, "/static/img/sprites/eggnog.png",
         "Creamy, spiced holiday beverage.", 1, 30),
        ("Holiday", "Glass of Milk", 1.49, "/static/img/sprites/glass_of_milk.png",
         "Fresh, cold milk. Perfect with cookies!", 1, 150),
        
        # Thanksgiving (Category: Holiday)
        ("Holiday", "Mashed Potatoes", 3.99, "/static/img/sprites/mashed_potatoes.png",
         "Creamy, buttery mashed potatoes.", 1, 25),
        ("Holiday", "Gravy", 1.99, "/static/img/sprites/gravy.png",
         "Rich, savory gravy for your potatoes and turkey.", 1, 40),
        ("Holiday", "Cranberry Sauce", 2.49, "/static/img/sprites/cranberry_sauce.png",
         "Tangy-sweet cranberry sauce, a holiday essential.", 0, 0),
    ]
    
    # Insert all food items
    cursor.executemany(
        "INSERT INTO items (category, name, price, imgurl, description, in_stock, stock_count) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);",
        food_items
    )
    
    # ── Demo Accounts ──────────────────────────────────────────────────
    #
    #  REGULAR USER
    #    Email:    user@foodshop.com
    #    Password: shopperpass
    #
    #  ADMIN
    #    Email:    admin@foodshop.com
    #    Password: adminpass
    #
    # ───────────────────────────────────────────────────────────────────

    demo_accounts = [
        ("user@foodshop.com",  "Jane Shopper", hash_password("shopperpass"), "user"),
        ("admin@foodshop.com", "Alex Admin",   hash_password("adminpass"),   "admin"),
    ]

    cursor.executemany(
        "INSERT INTO customers (email, name, password_hash, role) VALUES (?, ?, ?, ?);",
        demo_accounts
    )
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized with {len(food_items)} food items.")
    print(f"Created {len(demo_accounts)} demo accounts:")
    print()
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │  REGULAR USER                                    │")
    print("  │    Email:    user@foodshop.com                   │")
    print("  │    Password: shopperpass                         │")
    print("  │                                                  │")
    print("  │  ADMIN                                           │")
    print("  │    Email:    admin@foodshop.com                  │")
    print("  │    Password: adminpass                           │")
    print("  └──────────────────────────────────────────────────┘")
    print()
    print("Database saved to food.db")


if __name__ == "__main__":
    init_database()