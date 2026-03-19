# Food Shop

A Flask-based e-commerce demo application for selling food items. This project showcases basic web application functionality including product listings, shopping cart management, and user sessions.

![Food Shop](static/img/sprites/red_apple.png)

## Features

- **Product Catalog**: Browse a variety of food items organized by category
- **Product Details**: View detailed information about each item
- **Shopping Cart**: Add items to cart, adjust quantities, and manage your order
- **User Sessions**: Log in to personalize your experience
- **Flash Messages**: Receive feedback on your actions
- **Responsive Design**: Works on desktop and mobile devices

## Asset Credits

All pixel art food sprites used in this project are created by **MelancholyG**.

- **Artist Profile**: [https://melancholyg.itch.io/](https://melancholyg.itch.io/)
- **Asset Page**: [16x16 Pixel Art Food Sprites](https://melancholyg.itch.io/16x16-pixel-art-food-sprites)

Please support the artist if you use these assets in your own projects!

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd food_shop

    Create and activate a virtual environment

    On macOS/Linux:

    bash
    python3 -m venv venv
    source venv/bin/activate

    On Windows:

    bash
    python -m venv venv
    venv\Scripts\activate

    Install dependencies

    bash
    pip install -r requirements.txt

    Place the sprite sheet

    Place the Foods.png sprite sheet (128x96 pixels, 16x16 sprites) in the static/img/ directory.

    Parse the sprites

    bash
    python parse_sprites.py

    This will extract individual sprite images to static/img/sprites/.

    Initialize the database

    bash
    python init_db.py

    This creates food.db with all the food items.

Running the Application
Development Mode

bash
python app.py

The application will start on http://localhost:5000.
With Custom Port

bash
PORT=8080 python app.py

Using Flask CLI

bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

Project Structure

food_shop/
├── app.py              # Main Flask application
├── model.py            # Database models and queries
├── init_db.py          # Database initialization script
├── parse_sprites.py    # Sprite sheet parser
├── food.db             # SQLite database (generated)
├── requirements.txt    # Python dependencies
├── Procfile            # For deployment (Heroku, etc.)
├── README.md           # This file
├── static/
│   ├── css/
│   │   ├── style.css   # Main stylesheet
│   │   └── cover.css   # Landing page styles
│   └── img/
│       ├── Foods.png   # Original sprite sheet
│       └── sprites/    # Extracted sprites (generated)
└── templates/
    ├── base.html       # Base template with navbar/footer
    ├── index.html      # Landing page
    ├── all_items.html  # Product listing page
    ├── item_details.html # Single product view
    ├── cart.html       # Shopping cart
    └── login.html      # Login form

Usage Guide
Browsing Items

    Visit the homepage and click "Shop Now"
    Browse items by scrolling through the product grid
    Click on any item to see its details

Adding to Cart

    Click "Add to Cart" on any product
    You'll be redirected to your cart with a confirmation message
    Adding the same item again increases its quantity

Managing Cart

    View your cart by clicking "My Cart" in the navigation
    Remove items using the "Remove" button
    Clear all items with "Clear Cart"
    Proceed to checkout (demo only - no actual payment)

User Login

    Click "Log In" in the navigation
    Enter any name, email, and password
    Note: This is a demo - no actual authentication is performed

Notes

    No Payment Processing: The checkout feature is a placeholder. No actual payments are processed.
    Session Storage: Cart data is stored in browser sessions and will be lost when the session expires.
    Demo Authentication: The login system stores user info in the session without validation.

Development
Adding New Items

Edit init_db.py and add new entries to the food_items list:

python
("Category", "Item Name", 9.99, "/static/img/sprites/image.png",
 "Description of the item."),

Then re-run the initialization:

bash
python init_db.py

Modifying Styles

    static/css/style.css - Main application styles
    static/css/cover.css - Landing page styles

Template Inheritance

All pages extend base.html which provides:

    Navigation bar
    Flash message display
    Footer with credits
    Common CSS/JS includes

License

This project is for educational/demonstration purposes.

Pixel art assets are © MelancholyG - please check the original asset page for licensing terms.


---

## Summary of Changes Made

1. **Fixed the error**: In `login.html`, changed `type="btn btn-lg btn-primary btn-block"` to `class="btn btn-lg btn-primary btn-block"`

2. **Updated Python 2 syntax**: Changed `print melons` to `print()` function calls in `model.py`

3. **Renamed files**:
   - `melons.py` → `app.py`
   - `all_melons.html` → `all_items.html`
   - `melon_details.html` → `item_details.html`
   - Database: `melons.db` → `food.db`

4. **Created new files**:
   - `parse_sprites.py` - Extracts individual sprites from the sprite sheet
   - `init_db.py` - Initializes the database with food items

5. **Re-themed everything**:
   - Updated all "melon" references to "food"/"item"
   - Updated branding from "Ubermelon" to "Food Shop"
   - Added artist credits throughout

6. **Implemented missing features**:
   - Cart removal functionality (`/remove_from_cart/<index>`)
   - Cart clearing functionality (`/clear_cart`)
   - Proper session modification tracking
   - 404 error handling
   - Stock status display

7. **Updated requirements.txt** for Python 3 and added Pillow for sprite parsing

