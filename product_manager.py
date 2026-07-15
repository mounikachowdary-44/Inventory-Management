"""
product_manager.py
-------------------
Handles everything related to products: adding, viewing, searching,
updating, deleting, and stock adjustments (add stock / reduce stock /
low stock alerts).
"""

from .storage import load_data, save_data

LOW_STOCK_THRESHOLD = 10


class ProductManager:
    """Manages the product inventory and persists it to a JSON file."""

    def __init__(self, file_path="data/products.json"):
        self.file_path = file_path
        self.products = load_data(self.file_path, default=[])

    # ------------------------------------------------------------------
    # Persistence helper
    # ------------------------------------------------------------------
    def _save(self):
        save_data(self.file_path, self.products)

    # ------------------------------------------------------------------
    # Core product operations
    # ------------------------------------------------------------------
    def add_product(self, product_id, name, category, price, quantity, supplier):
        """Add a new product. Returns (success: bool, message: str)."""
        product_id = str(product_id).strip()

        if not product_id or not name.strip():
            return False, "❌ Product ID and Name cannot be empty."

        if self.find_by_id(product_id):
            return False, f"❌ Product ID '{product_id}' already exists."

        if price < 0:
            return False, "❌ Price cannot be negative."

        if quantity < 0:
            return False, "❌ Quantity cannot be negative."

        new_product = {
            "product_id": product_id,
            "name": name.strip(),
            "category": category.strip(),
            "price": round(float(price), 2),
            "quantity": int(quantity),
            "supplier": supplier.strip(),
        }
        self.products.append(new_product)
        self._save()
        return True, f"✅ Product '{name}' added successfully."

    def view_products(self):
        """Return the full list of products."""
        return self.products

    def find_by_id(self, product_id):
        """Return a product dict by ID, or None if not found."""
        product_id = str(product_id).strip()
        for product in self.products:
            if product["product_id"] == product_id:
                return product
        return None

    def search_products(self, keyword):
        """
        Search products by Product ID (exact match) or Product Name
        (case-insensitive partial match). Returns a list of matches.
        """
        keyword = str(keyword).strip().lower()
        results = []
        for product in self.products:
            if (product["product_id"].lower() == keyword or
                    keyword in product["name"].lower()):
                results.append(product)
        return results

    def update_product(self, product_id, name=None, price=None,
                        quantity=None, category=None):
        """Update selected fields of an existing product."""
        product = self.find_by_id(product_id)
        if not product:
            return False, f"❌ Product ID '{product_id}' not found."

        if name is not None and name.strip():
            product["name"] = name.strip()

        if category is not None and category.strip():
            product["category"] = category.strip()

        if price is not None:
            if price < 0:
                return False, "❌ Price cannot be negative."
            product["price"] = round(float(price), 2)

        if quantity is not None:
            if quantity < 0:
                return False, "❌ Quantity cannot be negative."
            product["quantity"] = int(quantity)

        self._save()
        return True, f"✅ Product '{product_id}' updated successfully."

    def delete_product(self, product_id):
        """Remove a product from inventory by Product ID."""
        product = self.find_by_id(product_id)
        if not product:
            return False, f"❌ Product ID '{product_id}' not found."

        self.products.remove(product)
        self._save()
        return True, f"✅ Product '{product_id}' deleted successfully."

    # ------------------------------------------------------------------
    # Stock management
    # ------------------------------------------------------------------
    def add_stock(self, product_id, quantity):
        """Increase the stock quantity of a product."""
        if quantity <= 0:
            return False, "❌ Quantity to add must be greater than zero."

        product = self.find_by_id(product_id)
        if not product:
            return False, f"❌ Product ID '{product_id}' not found."

        product["quantity"] += int(quantity)
        self._save()
        return True, (f"✅ Stock updated. '{product['name']}' now has "
                       f"{product['quantity']} units.")

    def reduce_stock(self, product_id, quantity):
        """
        Decrease the stock quantity of a product (e.g. after a sale).
        Returns (success, message).
        """
        if quantity <= 0:
            return False, "❌ Quantity to reduce must be greater than zero."

        product = self.find_by_id(product_id)
        if not product:
            return False, f"❌ Product ID '{product_id}' not found."

        if quantity > product["quantity"]:
            return False, (f"❌ Insufficient stock. Only "
                            f"{product['quantity']} unit(s) available.")

        product["quantity"] -= int(quantity)
        self._save()
        return True, (f"✅ Stock reduced. '{product['name']}' now has "
                       f"{product['quantity']} units.")

    def low_stock_alert(self, threshold=LOW_STOCK_THRESHOLD):
        """Return a list of products whose quantity is below threshold."""
        return [p for p in self.products if p["quantity"] < threshold]

    # ------------------------------------------------------------------
    # Reporting helpers
    # ------------------------------------------------------------------
    def inventory_report(self):
        """Return a dict summarising the current inventory."""
        total_products = len(self.products)
        categories = {p["category"] for p in self.products if p["category"]}
        total_stock = sum(p["quantity"] for p in self.products)

        return {
            "total_products": total_products,
            "total_categories": len(categories),
            "categories": sorted(categories),
            "total_available_stock": total_stock,
        }
