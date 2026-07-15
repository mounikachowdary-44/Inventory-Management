"""
main.py
--------
Entry point for the Inventory Management System.

Provides a menu-driven console interface that ties together the
ProductManager (products + stock) and SalesManager (sales + reports)
modules.

Run with:
    python main.py
"""

import os
import sys

from inventory.product_manager import ProductManager
from inventory.sales_manager import SalesManager

PRODUCTS_FILE = os.path.join("data", "products.json")
SALES_FILE = os.path.join("data", "sales.json")


# ----------------------------------------------------------------------
# Input helpers (centralised so every menu option handles bad input the
# same way instead of crashing the program).
# ----------------------------------------------------------------------
def get_non_empty_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ This field cannot be empty. Please try again.")


def get_optional_string(prompt):
    """Used for update flows where leaving blank means 'keep current value'."""
    return input(prompt).strip()


def get_float(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            value = float(raw)
            return value
        except ValueError:
            print("❌ Please enter a valid number.")


def get_int(prompt, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("❌ Please enter a valid whole number.")


# ----------------------------------------------------------------------
# Display helpers
# ----------------------------------------------------------------------
def print_products_table(products):
    if not products:
        print("\n(No products to display)\n")
        return

    headers = ["Product ID", "Name", "Category", "Price", "Quantity", "Supplier"]
    rows = [
        [p["product_id"], p["name"], p["category"],
         f"{p['price']:.2f}", p["quantity"], p["supplier"]]
        for p in products
    ]
    _print_table(headers, rows)


def print_sales_table(sales):
    if not sales:
        print("\n(No sales recorded yet)\n")
        return

    headers = ["Date", "Product ID", "Product Name", "Qty Sold", "Unit Price", "Total"]
    rows = [
        [s["date"], s["product_id"], s["product_name"], s["quantity_sold"],
         f"{s['unit_price']:.2f}", f"{s['total_amount']:.2f}"]
        for s in sales
    ]
    _print_table(headers, rows)


def _print_table(headers, rows):
    """Simple dependency-free table printer (falls back cleanly without
    needing the optional 'tabulate' package)."""
    try:
        from tabulate import tabulate
        print("\n" + tabulate(rows, headers=headers, tablefmt="grid") + "\n")
        return
    except ImportError:
        pass

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    def format_row(row):
        return " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))

    separator = "-+-".join("-" * w for w in col_widths)

    print()
    print(format_row(headers))
    print(separator)
    for row in rows:
        print(format_row(row))
    print()


def print_menu():
    print("=" * 45)
    print(" 📦 INVENTORY MANAGEMENT SYSTEM ")
    print("=" * 45)
    print("1. Add Product")
    print("2. View Products")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Add Stock")
    print("7. Record Sale")
    print("8. Inventory Report")
    print("9. Sales Report")
    print("10. Low Stock Alert")
    print("11. Exit")
    print("=" * 45)


# ----------------------------------------------------------------------
# Menu option handlers
# ----------------------------------------------------------------------
def handle_add_product(product_manager):
    print("\n--- Add New Product ---")
    product_id = get_non_empty_string("Product ID: ")
    name = get_non_empty_string("Product Name: ")
    category = get_non_empty_string("Category: ")
    price = get_float("Price: ")
    quantity = get_int("Quantity Available: ")
    supplier = get_non_empty_string("Supplier Name: ")

    success, message = product_manager.add_product(
        product_id, name, category, price, quantity, supplier
    )
    print(message)


def handle_view_products(product_manager):
    print("\n--- All Products ---")
    print_products_table(product_manager.view_products())


def handle_search_product(product_manager):
    print("\n--- Search Product ---")
    keyword = get_non_empty_string("Enter Product ID or Name to search: ")
    results = product_manager.search_products(keyword)
    if results:
        print(f"\nFound {len(results)} matching product(s):")
        print_products_table(results)
    else:
        print("❌ No matching products found.")


def handle_update_product(product_manager):
    print("\n--- Update Product ---")
    product_id = get_non_empty_string("Enter Product ID to update: ")

    product = product_manager.find_by_id(product_id)
    if not product:
        print(f"❌ Product ID '{product_id}' not found.")
        return

    print(f"Current details: {product}")
    print("(Press Enter to keep the current value for any field)")

    name = get_optional_string(f"New Name [{product['name']}]: ")
    category = get_optional_string(f"New Category [{product['category']}]: ")
    price = get_float(f"New Price [{product['price']}]: ", allow_blank=True)
    quantity = get_int(f"New Quantity [{product['quantity']}]: ", allow_blank=True)

    success, message = product_manager.update_product(
        product_id,
        name=name or None,
        price=price,
        quantity=quantity,
        category=category or None,
    )
    print(message)


def handle_delete_product(product_manager):
    print("\n--- Delete Product ---")
    product_id = get_non_empty_string("Enter Product ID to delete: ")
    confirm = input(f"Are you sure you want to delete '{product_id}'? (y/n): ").strip().lower()
    if confirm == "y":
        success, message = product_manager.delete_product(product_id)
        print(message)
    else:
        print("Deletion cancelled.")


def handle_add_stock(product_manager):
    print("\n--- Add Stock ---")
    product_id = get_non_empty_string("Product ID: ")
    quantity = get_int("Quantity to Add: ")
    success, message = product_manager.add_stock(product_id, quantity)
    print(message)


def handle_record_sale(sales_manager):
    print("\n--- Record Sale ---")
    product_id = get_non_empty_string("Product ID: ")
    quantity = get_int("Quantity Sold: ")
    success, message = sales_manager.record_sale(product_id, quantity)
    print(message)


def handle_inventory_report(product_manager):
    print("\n--- Inventory Report ---")
    report = product_manager.inventory_report()
    print(f"Total Products     : {report['total_products']}")
    print(f"Total Categories   : {report['total_categories']} {report['categories']}")
    print(f"Total Available Stock: {report['total_available_stock']}")


def handle_sales_report(sales_manager):
    print("\n--- Sales Report ---")
    report = sales_manager.sales_report()
    print(f"Total Sales Transactions : {report['total_sales_transactions']}")
    print(f"Total Products Sold      : {report['total_products_sold']}")
    print(f"Total Revenue Generated  : ₹{report['total_revenue']:.2f}")
    print(f"Most Sold Product        : {report['most_sold_product'] or 'N/A'}")


def handle_low_stock_alert(product_manager):
    print(f"\n--- Low Stock Alert (below {10} units) ---")
    low_stock_products = product_manager.low_stock_alert()
    if low_stock_products:
        print_products_table(low_stock_products)
    else:
        print("✅ All products have sufficient stock.")


# ----------------------------------------------------------------------
# Main application loop
# ----------------------------------------------------------------------
def main():
    product_manager = ProductManager(file_path=PRODUCTS_FILE)
    sales_manager = SalesManager(product_manager, file_path=SALES_FILE)

    menu_actions = {
        "1": lambda: handle_add_product(product_manager),
        "2": lambda: handle_view_products(product_manager),
        "3": lambda: handle_search_product(product_manager),
        "4": lambda: handle_update_product(product_manager),
        "5": lambda: handle_delete_product(product_manager),
        "6": lambda: handle_add_stock(product_manager),
        "7": lambda: handle_record_sale(sales_manager),
        "8": lambda: handle_inventory_report(product_manager),
        "9": lambda: handle_sales_report(sales_manager),
        "10": lambda: handle_low_stock_alert(product_manager),
    }

    while True:
        print_menu()
        choice = input("Enter your choice (1-11): ").strip()

        if choice == "11":
            print("\n👋 Exiting Inventory Management System. Goodbye!")
            sys.exit(0)

        action = menu_actions.get(choice)
        if action:
            try:
                action()
            except Exception as error:  # noqa: BLE001 - top-level safety net
                print(f"❌ An unexpected error occurred: {error}")
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 11.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
