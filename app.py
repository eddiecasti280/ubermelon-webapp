#!/usr/bin/env python3
"""
Food Shop - A Flask-based e-commerce platform for food items.

Features:
  - Product listing and details
  - Shopping cart with session management
  - User authentication with role-based access
  - Admin inventory dashboard
  - Flash messages for user feedback
"""

from functools import wraps
from flask import (Flask, request, session, render_template,
                   redirect, url_for, flash, abort)
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined


# ── Decorators ──────────────────────────────────────────────────────

def login_required(f):
    """Redirect to login page if the user is not authenticated."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access that page.")
            return redirect(url_for('show_login'))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """Return 403 if the current user is not an admin."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access that page.")
            return redirect(url_for('show_login'))
        if session.get('role') != 'admin':
            flash("Access denied. Admin privileges required.")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapper


# ── Public Routes ───────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing page for the Food Shop."""
    return render_template("index.html")


@app.route("/items")
def list_items():
    """Display all available food items."""
    items = model.get_items()
    return render_template("all_items.html", item_list=items)


@app.route("/item/<int:id>")
def show_item(id):
    """Display details for a specific food item."""
    item = model.get_item_by_id(id)
    if item is None:
        flash("Item not found!")
        return redirect(url_for('list_items'))
    return render_template("item_details.html", display_item=item)


# ── Cart Routes ─────────────────────────────────────────────────────

@app.route("/cart")
def shopping_cart():
    """Display the contents of the shopping cart."""
    if 'cart' not in session:
        session['cart'] = []
    items_in_cart = session['cart']
    total = get_total()
    return render_template("cart.html", items_in_cart=items_in_cart, total=total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a food item to the shopping cart."""
    item = model.get_item_by_id(id)
    if item is None:
        flash("Item not found!")
        return redirect(url_for('list_items'))

    item_name = item.name
    item_price = item.price

    if 'cart' not in session:
        session['cart'] = []

    for cart_item in session['cart']:
        if cart_item[0] == item_name:
            cart_item[1] = cart_item[1] + 1
            session.modified = True
            flash(f'Increased quantity of {item_name} in your cart.')
            return redirect(url_for('shopping_cart'))

    session['cart'].append([item_name, 1, item_price])
    session.modified = True
    flash(f'Successfully added {item_name} to your cart.')
    return redirect(url_for('shopping_cart'))


@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    """Remove an item from the shopping cart by index."""
    if 'cart' in session and 0 <= index < len(session['cart']):
        removed_item = session['cart'].pop(index)
        session.modified = True
        flash(f'Removed {removed_item[0]} from your cart.')
    return redirect(url_for('shopping_cart'))


@app.route("/clear_cart")
def clear_cart():
    """Clear all items from the shopping cart."""
    session['cart'] = []
    session.modified = True
    flash('Your cart has been cleared.')
    return redirect(url_for('shopping_cart'))


def get_total():
    """Calculate the total price of all items in the cart."""
    total = 0.0
    if 'cart' in session and len(session['cart']) > 0:
        for item in session['cart']:
            total += item[2] * item[1]
    return round(total, 2)


# ── Auth Routes ─────────────────────────────────────────────────────

@app.route("/login", methods=['GET'])
def show_login():
    """Display the login form."""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """
    Authenticate the user against the database.

    On success the session is populated with user_id, name, email, and role.
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash("Please provide both email and password.")
        return redirect(url_for('show_login'))

    customer = model.authenticate_customer(email, password)

    if customer is None:
        flash("Invalid email or password. Please try again.")
        return redirect(url_for('show_login'))

    # Store user info in the session
    session['user_id'] = customer.id
    session['name'] = customer.name
    session['email'] = customer.email
    session['role'] = customer.role

    flash(f'Welcome back, {customer.name}!')

    if customer.is_admin():
        return redirect(url_for('admin_inventory'))

    return redirect(url_for('list_items'))


@app.route("/logout")
def process_logout():
    """Log out the current user."""
    for key in ('user_id', 'name', 'email', 'role', 'password'):
        session.pop(key, None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


# ── Checkout ────────────────────────────────────────────────────────

@app.route("/checkout")
def checkout():
    """Mock checkout – no actual payment is processed."""
    if 'cart' not in session or len(session['cart']) == 0:
        flash("Your cart is empty!")
        return redirect(url_for('shopping_cart'))

    flash("Thank you for your order! "
          "(Note: Payment processing is not implemented in this demo.)")
    session['cart'] = []
    session.modified = True
    return redirect(url_for('list_items'))


# ── Admin Routes ────────────────────────────────────────────────────

@app.route("/admin")
@admin_required
def admin_inventory():
    """
    Admin dashboard showing full inventory overview.
    Only accessible to users whose role is 'admin'.
    """
    summary = model.get_inventory_summary()
    categories = model.get_all_categories()
    return render_template("admin_inventory.html",
                           summary=summary,
                           categories=categories)


@app.route("/admin/item/<int:id>")
@admin_required
def admin_item_detail(id):
    """Admin view of a single item with editable details."""
    item = model.get_item_by_id(id)
    if item is None:
        flash("Item not found!")
        return redirect(url_for('admin_inventory'))
    categories = model.get_all_categories()
    return render_template("admin_item_detail.html",
                           item=item, categories=categories)


@app.route("/admin/item/<int:id>/update", methods=["POST"])
@admin_required
def admin_update_item(id):
    """Process the admin edit-item form."""
    name = request.form.get('name', '').strip()
    price = request.form.get('price', type=float)
    category = request.form.get('category', '').strip()
    description = request.form.get('description', '').strip()
    stock_count = request.form.get('stock_count', type=int)
    in_stock = 'in_stock' in request.form

    if not name or price is None or stock_count is None:
        flash("Please fill in all required fields.")
        return redirect(url_for('admin_item_detail', id=id))

    success = model.update_item(id, name, price, category,
                                description, stock_count, in_stock)

    if success:
        flash(f'Item "{name}" updated successfully.')
    else:
        flash("Update failed. Item may not exist.")

    return redirect(url_for('admin_item_detail', id=id))


@app.route("/admin/item/<int:id>/quick_stock", methods=["POST"])
@admin_required
def admin_quick_stock(id):
    """Quick stock-count update from the inventory table."""
    stock_count = request.form.get('stock_count', type=int)
    if stock_count is None or stock_count < 0:
        flash("Invalid stock count.")
        return redirect(url_for('admin_inventory'))

    in_stock = stock_count > 0
    success = model.update_item_stock(id, stock_count, in_stock)

    if success:
        item = model.get_item_by_id(id)
        flash(f'Stock for "{item.name}" updated to {stock_count}.')
    else:
        flash("Update failed.")

    return redirect(url_for('admin_inventory'))


# ── Error Handlers ──────────────────────────────────────────────────

@app.errorhandler(404)
def page_not_found(e):
    flash("Page not found!")
    return redirect(url_for('index'))


@app.errorhandler(403)
def forbidden(e):
    flash("Access denied.")
    return redirect(url_for('index'))


# ── Entry Point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port, host='0.0.0.0')