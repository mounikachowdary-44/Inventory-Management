"""
app.py
-------
Flask web front-end for the Inventory Management System.

Reuses the same business logic (ProductManager / SalesManager) that
powers the console version — only the interface layer changes, from
input()/print() to HTTP routes and HTML templates.

Local run:
    python app.py

Production (used by Render):
    gunicorn app:app
"""

import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from inventory.product_manager import ProductManager
from inventory.sales_manager import SalesManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
SALES_FILE = os.path.join(DATA_DIR, "sales.json")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

product_manager = ProductManager(file_path=PRODUCTS_FILE)
sales_manager = SalesManager(product_manager, file_path=SALES_FILE)


def today_stamp():
    return datetime.now().strftime("%d %b %Y")


# ----------------------------------------------------------------------
# Dashboard / product list
# ----------------------------------------------------------------------
@app.route("/")
def dashboard():
    products = product_manager.view_products()
    report = product_manager.inventory_report()
    low_stock_count = len(product_manager.low_stock_alert())
    return render_template(
        "dashboard.html",
        active="dashboard",
        products=products,
        report=report,
        low_stock_count=low_stock_count,
        today=today_stamp(),
    )


# ----------------------------------------------------------------------
# Add product
# ----------------------------------------------------------------------
@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        try:
            product_id = request.form.get("product_id", "")
            name = request.form.get("name", "")
            category = request.form.get("category", "")
            price = float(request.form.get("price", 0))
            quantity = int(request.form.get("quantity", 0))
            supplier = request.form.get("supplier", "")

            success, message = product_manager.add_product(
                product_id, name, category, price, quantity, supplier
            )
            flash(message, "success" if success else "error")
            if success:
                return redirect(url_for("dashboard"))
        except (ValueError, TypeError):
            flash("❌ Please enter valid numeric values for price and quantity.", "error")

    return render_template("add_product.html", active="add_product")


# ----------------------------------------------------------------------
# Edit product
# ----------------------------------------------------------------------
@app.route("/products/<product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = product_manager.find_by_id(product_id)
    if not product:
        flash(f"❌ Product ID '{product_id}' not found.", "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        try:
            name = request.form.get("name", "")
            category = request.form.get("category", "")
            price = float(request.form.get("price", 0))
            quantity = int(request.form.get("quantity", 0))

            success, message = product_manager.update_product(
                product_id, name=name, price=price, quantity=quantity, category=category
            )
            flash(message, "success" if success else "error")
            if success:
                return redirect(url_for("dashboard"))
        except (ValueError, TypeError):
            flash("❌ Please enter valid numeric values for price and quantity.", "error")

    return render_template("edit_product.html", active="dashboard", product=product)


# ----------------------------------------------------------------------
# Delete product
# ----------------------------------------------------------------------
@app.route("/products/<product_id>/delete", methods=["POST"])
def delete_product(product_id):
    success, message = product_manager.delete_product(product_id)
    flash(message, "success" if success else "error")
    return redirect(url_for("dashboard"))


# ----------------------------------------------------------------------
# Search product
# ----------------------------------------------------------------------
@app.route("/products/search")
def search_product():
    query = request.args.get("q", "").strip()
    results = product_manager.search_products(query) if query else []
    return render_template(
        "search.html", active="dashboard", query=query, results=results
    )


# ----------------------------------------------------------------------
# Add stock
# ----------------------------------------------------------------------
@app.route("/stock/add", methods=["GET", "POST"])
def add_stock():
    if request.method == "POST":
        product_id = request.form.get("product_id", "")
        try:
            quantity = int(request.form.get("quantity", 0))
            success, message = product_manager.add_stock(product_id, quantity)
            flash(message, "success" if success else "error")
            if success:
                return redirect(url_for("dashboard"))
        except (ValueError, TypeError):
            flash("❌ Please enter a valid whole number for quantity.", "error")

    return render_template(
        "add_stock.html", active="stock", products=product_manager.view_products()
    )


# ----------------------------------------------------------------------
# Record sale
# ----------------------------------------------------------------------
@app.route("/sales/record", methods=["GET", "POST"])
def record_sale():
    if request.method == "POST":
        product_id = request.form.get("product_id", "")
        try:
            quantity = int(request.form.get("quantity", 0))
            success, message = sales_manager.record_sale(product_id, quantity)
            flash(message, "success" if success else "error")
            if success:
                return redirect(url_for("sales_history"))
        except (ValueError, TypeError):
            flash("❌ Please enter a valid whole number for quantity.", "error")

    return render_template(
        "record_sale.html", active="sale", products=product_manager.view_products()
    )


# ----------------------------------------------------------------------
# Sales history
# ----------------------------------------------------------------------
@app.route("/sales")
def sales_history():
    sales = list(reversed(sales_manager.view_sales()))
    return render_template("sales_history.html", active="sales", sales=sales)


# ----------------------------------------------------------------------
# Reports
# ----------------------------------------------------------------------
@app.route("/reports")
def reports():
    return render_template(
        "reports.html",
        active="reports",
        inv=product_manager.inventory_report(),
        sales=sales_manager.sales_report(),
        today=today_stamp(),
    )


# ----------------------------------------------------------------------
# Low stock alert
# ----------------------------------------------------------------------
@app.route("/low-stock")
def low_stock():
    return render_template(
        "low_stock.html", active="low_stock", products=product_manager.low_stock_alert()
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
