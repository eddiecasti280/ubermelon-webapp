# Food Shop

A Flask-based e-commerce demo application for selling food items. This project showcases basic web application functionality including product listings, shopping cart management, user sessions, and an admin inventory dashboard.

## Features

- **Product Catalog**: Browse a variety of food items organized by category
- **Product Details**: View detailed information about each item with interactive 3D sprite effects
- **Shopping Cart**: Add items to cart, adjust quantities, and manage your order
- **User Authentication**: Log in with credentials verified against the database
- **Admin Inventory Dashboard**: View stock levels, edit items, and manage inventory (admin only)
- **Role-Based Access**: Regular users shop; admins access the inventory management panel
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

    Place the Foods.png sprite sheet (128×96 pixels, 16×16 sprites) in the static/img/ directory.

    Parse the sprites

    bash
    python parse_sprites.py

    This will extract individual sprite images into static/img/sprites/.

    Initialize the database

    bash
    python init_db.py

    This creates food.db with all food items and the demo accounts shown below.

Running the Application
Development Mode

bash
python app.py

The application will start on http://localhost:5000.
With Custom Port

bash
PORT=8080 python app.py

Demo Accounts

The database ships with two pre-configured accounts for testing:

Role	Email	Password
Regular User	user@foodshop.com	shopperpass
Admin	admin@foodshop.com	adminpass

Regular User – user@foodshop.com

    Browse and view all products
    Add items to the shopping cart
    Proceed through the (mock) checkout flow

Admin – admin@foodshop.com

    Everything a regular user can do, plus:
    Access the Inventory Dashboard (/admin) from the navbar
    View total stock counts, stock value, and per-item quantities
    Quick-update stock counts directly from the inventory table
    Open a full edit form for any item (name, price, category, description, stock, availability)

Project Structure

food_shop/
├── app.py                     # Main Flask application with routes
├── model.py                   # Database models and queries
├── init_db.py                 # Database initialization & demo data
├── parse_sprites.py           # Sprite sheet parser
├── food.db                    # SQLite database (generated)
├── requirements.txt           # Python dependencies
├── Procfile                   # For deployment (Heroku, etc.)
├── README.md                  # This file
├── static/
│   ├── css/
│   │   ├── style.css          # Main stylesheet
│   │   └── cover.css          # Landing page styles
│   └── img/
│       ├── Foods.png          # Original sprite sheet
│       └── sprites/           # Extracted sprites (generated)
└── templates/
    ├── base.html              # Base template with navbar/footer
    ├── index.html             # Landing page
    ├── all_items.html         # Product listing page
    ├── item_details.html      # Single product view
    ├── cart.html              # Shopping cart
    ├── login.html             # Login form
    ├── admin_inventory.html   # Admin inventory dashboard
    └── admin_item_detail.html # Admin item edit form

Usage Guide
Browsing Items

    Visit the homepage and click Shop Now
    Browse items in the product grid
    Click any item to see its details — hover near the sprite to see the 3D tilt effect

Shopping Cart

    Click Add to Cart on any product
    You'll be redirected to your cart with a confirmation
    Adding the same item again increases its quantity
    Remove individual items or clear the whole cart

Admin Inventory (admin@foodshop.com / adminpass)

    Log in with admin credentials
    Click ★ Inventory in the navbar
    The dashboard shows summary cards (total products, units, value, in/out of stock)
    Each category section lists items with inline stock editing
    Click Edit on any row to open the full edit form
    Changes are saved to the database immediately

Notes

    No Payment Processing: The checkout feature is a placeholder. No actual payments are processed.
    Session Storage: Cart data is stored in browser sessions and will be lost when the session expires.
    Demo Authentication: Passwords are hashed with SHA-256 for this demo. A production application should use bcrypt or argon2.
    Admin Protection: All /admin/* routes are protected by the @admin_required decorator, which checks both that the user is logged in and that their role is 'admin'.

License

This project is for educational/demonstration purposes.

Pixel art assets are © MelancholyG — please check the original asset page for licensing terms.


The main additions:

1. **Database-backed authentication** – `model.authenticate_customer()` verifies email + SHA-256-hashed password. The old "type any name" form is replaced with a proper credential check.

2. **Role system** – The `customers` table has a `role` column (`'user'` or `'admin'`). Session stores the role after login.

3. **`@login_required` and `@admin_required` decorators** – Protect routes cleanly. Admin routes return a flash + redirect if the user lacks privileges.

4. **Admin inventory dashboard** (`/admin`) – Summary cards showing total products, units, stock value, and in/out-of-stock counts. Per-category tables with inline quick-stock editing and links to a full edit form.

5. **Admin item editor** (`/admin/item/<id>`) – Full form to change name, price, category, description, stock count, and availability. Updates write through to the database via `model.update_item()`.

6. **Demo credentials on the login page** – Clearly displayed so anyone can test both roles. The `name` field was removed from login since authentication now goes through the database.

7. **Two hardcoded demo accounts** created by `init_db.py`:
   - **User**: `user@foodshop.com` / `shopperpass`  
   - **Admin**: `admin@foodshop.com` / `adminpass`