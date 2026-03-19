#!/usr/bin/env python3
"""
Database initialization script for Food Shop.

This script creates the SQLite database and populates it with food items
based on the parsed sprite images.
"""

import sqlite3
import os


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
            in_stock INTEGER DEFAULT 1
        );
    """)
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT
        );
    """)
    
    # Food item data based on the sprite sheet
    food_items = [
        # Apples (Category: Fruit)
        ("Fruit", "Red Apple", 0.99, "/static/img/sprites/red_apple.png",
         "A classic red apple, sweet and crispy. Perfect for snacking or baking."),
        ("Fruit", "Granny Smith Apple", 1.09, "/static/img/sprites/granny_smith_apple.png",
         "Tart and tangy green apple. Great for pies and salads."),
        ("Fruit", "Golden Delicious Apple", 1.19, "/static/img/sprites/golden_delicious_apple.png",
         "Sweet yellow apple with a mild flavor. Excellent eating apple."),
        ("Fruit", "Ambrosia Apple", 1.49, "/static/img/sprites/ambrosia_apple.png",
         "Sweet and aromatic apple with honey-like flavor notes."),
        ("Fruit", "Honeycrisp Apple", 1.79, "/static/img/sprites/honeycrisp_apple.png",
         "Exceptionally crisp and juicy with balanced sweet-tart flavor."),
        ("Fruit", "Half Apple", 0.59, "/static/img/sprites/half_apple.png",
         "Pre-cut apple half, perfect for quick snacks."),
        
        # Pears (Category: Fruit)
        ("Fruit", "Concorde Pear", 1.29, "/static/img/sprites/concorde_pear.png",
         "Sweet vanilla-flavored pear that doesn't brown quickly when cut."),
        ("Fruit", "Bartlett Pear", 1.19, "/static/img/sprites/bartlett_pear.png",
         "Classic pear with smooth, sweet flesh. Great for canning."),
        ("Fruit", "Bosk Pear", 1.39, "/static/img/sprites/bosk_pear.png",
         "Firm, dense pear with warm spice and honey undertones."),
        ("Fruit", "Chinese White Pear", 1.59, "/static/img/sprites/chinese_white_pear.png",
         "Crisp Asian pear with refreshing, light sweetness."),
        ("Fruit", "Forelle Pear", 1.49, "/static/img/sprites/forelle_pear.png",
         "Small, sweet pear with distinctive red freckling."),
        ("Fruit", "Seckel Pear", 0.99, "/static/img/sprites/seckel_pear.png",
         "Tiny 'sugar pear' with intense sweetness. Perfect bite-sized treat."),
        ("Fruit", "Conference Pear", 1.29, "/static/img/sprites/conference_pear.png",
         "Long, slender pear with sweet, slightly tangy flavor."),
        
        # Vegetables (Category: Vegetable)
        ("Vegetable", "Tomato", 0.79, "/static/img/sprites/tomato.png",
         "Ripe red tomato, perfect for salads, sandwiches, or cooking."),
        ("Vegetable", "Yellow Tomato", 0.89, "/static/img/sprites/yellow_tomato.png",
         "Milder, less acidic tomato variety with sunny color."),
        ("Vegetable", "Pumpkin", 4.99, "/static/img/sprites/pumpkin.png",
         "Perfect for pies, soups, or autumn decoration."),
        ("Vegetable", "Carrot", 0.49, "/static/img/sprites/carrot.png",
         "Fresh, crunchy carrot. Great raw or cooked."),
        ("Vegetable", "Pea Pod", 2.49, "/static/img/sprites/pea_pod.png",
         "Fresh snap peas in the pod. Sweet and crunchy."),
        ("Vegetable", "Bell Pepper", 1.29, "/static/img/sprites/bell_pepper.png",
         "Crisp red bell pepper, sweet and versatile."),
        ("Vegetable", "Yellow Bell Pepper", 1.29, "/static/img/sprites/yellow_bell_pepper.png",
         "Sweet yellow bell pepper, milder than green varieties."),
        ("Vegetable", "Green Bell Pepper", 0.99, "/static/img/sprites/green_bell_pepper.png",
         "Classic green bell pepper with slightly bitter, fresh taste."),
        
        # Breakfast/Fast Food (Category: Prepared Food)
        ("Prepared Food", "Scrambled Egg", 2.99, "/static/img/sprites/scrambled_egg.png",
         "Fluffy scrambled eggs, made fresh to order."),
        ("Prepared Food", "Bacon", 3.49, "/static/img/sprites/bacon.png",
         "Strips of perfectly cooked bacon."),
        ("Prepared Food", "Crispy Bacon", 3.99, "/static/img/sprites/crispy_bacon.png",
         "Extra crispy bacon for those who like it crunchy."),
        ("Prepared Food", "Cheese", 2.99, "/static/img/sprites/cheese.png",
         "Slice of quality cheese, perfect for sandwiches."),
        ("Prepared Food", "Pizza Slice", 3.49, "/static/img/sprites/pizza_slice.png",
         "Hot slice of pepperoni pizza."),
        ("Prepared Food", "Hot Dog", 2.99, "/static/img/sprites/hot_dog.png",
         "Classic hot dog with all the fixings."),
        
        # Holiday Treats (Category: Holiday)
        ("Holiday", "Candy Cane", 0.99, "/static/img/sprites/candy_cane.png",
         "Traditional peppermint candy cane. Festive and sweet!"),
        ("Holiday", "Gingerbread Man", 2.49, "/static/img/sprites/gingerbread_man.png",
         "Decorated gingerbread cookie shaped like a person."),
        ("Holiday", "Gingerbread Man Base", 1.99, "/static/img/sprites/gingerbread_man_base.png",
         "Undecorated gingerbread cookie - decorate it yourself!"),
        ("Holiday", "Gingerbread House", 12.99, "/static/img/sprites/gingerbread_house.png",
         "Beautiful edible gingerbread house kit."),
        ("Holiday", "Glühwein", 4.99, "/static/img/sprites/glintwein.png",
         "Traditional mulled wine with warm spices."),
        ("Holiday", "Eggnog", 3.99, "/static/img/sprites/eggnog.png",
         "Creamy, spiced holiday beverage."),
        ("Holiday", "Glass of Milk", 1.49, "/static/img/sprites/glass_of_milk.png",
         "Fresh, cold milk. Perfect with cookies!"),
        
        # Thanksgiving (Category: Holiday)
        ("Holiday", "Mashed Potatoes", 3.99, "/static/img/sprites/mashed_potatoes.png",
         "Creamy, buttery mashed potatoes."),
        ("Holiday", "Gravy", 1.99, "/static/img/sprites/gravy.png",
         "Rich, savory gravy for your potatoes and turkey."),
        ("Holiday", "Cranberry Sauce", 2.49, "/static/img/sprites/cranberry_sauce.png",
         "Tangy-sweet cranberry sauce, a holiday essential."),
    ]
    
    # Insert all food items
    cursor.executemany(
        "INSERT INTO items (category, name, price, imgurl, description, in_stock) VALUES (?, ?, ?, ?, ?, 1);",
        food_items
    )
    
    # Add a sample customer
    cursor.execute(
        "INSERT INTO customers (email, name) VALUES (?, ?);",
        ("test@example.com", "Test User")
    )
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized with {len(food_items)} food items.")
    print("Database saved to food.db")


if __name__ == "__main__":
    init_database()