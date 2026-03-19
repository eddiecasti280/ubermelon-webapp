#!/usr/bin/env python3
"""
Food Shop - A Flask-based e-commerce platform for food items.

This application demonstrates basic e-commerce functionality including:
- Product listing and details
- Shopping cart with session management
- User authentication (mock implementation)
- Flash messages for user feedback
"""

from flask import Flask, request, session, render_template, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """
    Landing page for the Food Shop.
    Displays the cover page with branding and shop features.
    """
    return render_template("index.html")


@app.route("/items")
def list_items():
    """
    Display all available food items.
    Queries the database for all items and renders them in a grid layout.
    """
    items = model.get_items()
    return render_template("all_items.html", item_list=items)


@app.route("/item/<int:id>")
def show_item(id):
    """
    Display details for a specific food item.
    
    Args:
        id: The unique identifier for the food item.
    
    Shows item details including name, price, category, and description.
    Provides option to add the item to the shopping cart.
    """
    item = model.get_item_by_id(id)
    if item is None:
        flash("Item not found!")
        return redirect(url_for('list_items'))
    return render_template("item_details.html", display_item=item)


@app.route("/cart")
def shopping_cart():
    """
    Display the contents of the shopping cart.
    
    The shopping cart is stored in the session as a list of items.
    Each item in the cart contains: [name, quantity, price]
    """
    if 'cart' not in session:
        session['cart'] = []
    
    items_in_cart = session['cart']
    total = get_total()
    
    return render_template("cart.html", items_in_cart=items_in_cart, total=total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """
    Add a food item to the shopping cart.
    
    Args:
        id: The unique identifier for the food item to add.
    
    If the item already exists in the cart, increments its quantity.
    Otherwise, adds a new entry with quantity 1.
    Displays appropriate flash message and redirects to cart.
    """
    item = model.get_item_by_id(id)
    
    if item is None:
        flash("Item not found!")
        return redirect(url_for('list_items'))
    
    item_name = item.name
    item_price = item.price

    if 'cart' not in session:
        session['cart'] = []
    
    # Check if item already in cart
    for cart_item in session['cart']:
        if cart_item[0] == item_name:
            cart_item[1] = cart_item[1] + 1
            session.modified = True
            flash(f'Increased quantity of {item_name} in your cart.')
            return redirect(url_for('shopping_cart'))

    # Add new item to cart
    session['cart'].append([item_name, 1, item_price])
    session.modified = True
    flash(f'Successfully added {item_name} to your cart.')
    return redirect(url_for('shopping_cart'))


@app.route("/remove_from_cart/<int:index>")
def remove_from_cart(index):
    """
    Remove an item from the shopping cart.
    
    Args:
        index: The index of the item in the cart list.
    """
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
    """
    Calculate the total price of all items in the cart.
    
    Returns:
        float: The total price of all items (price * quantity).
    """
    total = 0.0
    if 'cart' in session and len(session['cart']) > 0:
        for item in session['cart']:
            total += item[2] * item[1]
    return round(total, 2)


@app.route("/login", methods=['GET'])
def show_login():
    """Display the login form."""
    return render_template("login.html")


@app.route("/logout")
def process_logout():
    """
    Log out the current user.
    Clears user information from the session and redirects to home.
    """
    if 'name' in session:
        del session['name']
    if 'email' in session:
        del session['email']
    if 'password' in session:
        del session['password']
    
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route("/login", methods=["POST"])
def process_login():
    """
    Process the login form submission.
    
    Note: This is a mock implementation that stores user info in session
    without actual authentication. In a production environment, you would
    validate credentials against a database and use proper password hashing.
    """
    session['email'] = request.form.get('email', '')
    session['password'] = request.form.get('password', '')
    session['name'] = request.form.get('name', '')

    if session['email'] and session['name']:
        flash(f'Welcome, {session["name"]}! You are now logged in.')
    else:
        flash('Please provide both name and email.')
        return redirect(url_for('show_login'))
    
    return redirect(url_for('list_items'))


@app.route("/checkout")
def checkout():
    """
    Process checkout (mock implementation).
    
    Note: Actual payment processing is not implemented.
    This redirects to the items page with a message.
    """
    if 'cart' not in session or len(session['cart']) == 0:
        flash("Your cart is empty!")
        return redirect(url_for('shopping_cart'))
    
    flash("Thank you for your order! (Note: Payment processing is not implemented in this demo.)")
    session['cart'] = []
    session.modified = True
    return redirect(url_for('list_items'))


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    flash("Page not found!")
    return redirect(url_for('index'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port, host='0.0.0.0')