"""
sales_manager.py
------------------
Handles recording sales transactions and generating sales reports/summaries.
Works together with ProductManager to update stock quantities whenever a
sale is recorded.
"""

from datetime import datetime
from .storage import load_data, save_data


class SalesManager:
    """Manages sales transactions and persists them to a JSON file."""

    def __init__(self, product_manager, file_path="data/sales.json"):
        self.file_path = file_path
        self.product_manager = product_manager
        self.sales = load_data(self.file_path, default=[])

    # ------------------------------------------------------------------
    # Persistence helper
    # ------------------------------------------------------------------
    def _save(self):
        save_data(self.file_path, self.sales)

    # ------------------------------------------------------------------
    # Core sales operations
    # ------------------------------------------------------------------
    def record_sale(self, product_id, quantity_sold):
        """
        Record a sale for a product: reduces stock and logs the
        transaction (with total amount and timestamp).

        Returns (success: bool, message: str).
        """
        if quantity_sold <= 0:
            return False, "❌ Quantity sold must be greater than zero."

        product = self.product_manager.find_by_id(product_id)
        if not product:
            return False, f"❌ Product ID '{product_id}' not found."

        success, message = self.product_manager.reduce_stock(
            product_id, quantity_sold
        )
        if not success:
            return False, message

        total_amount = round(product["price"] * quantity_sold, 2)
        sale_record = {
            "product_id": product["product_id"],
            "product_name": product["name"],
            "quantity_sold": int(quantity_sold),
            "unit_price": product["price"],
            "total_amount": total_amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.sales.append(sale_record)
        self._save()

        return True, (f"✅ Sale recorded: {quantity_sold} x '{product['name']}' "
                       f"= ₹{total_amount:.2f}")

    def view_sales(self):
        """Return the full list of recorded sales."""
        return self.sales

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def sales_summary(self):
        """Return total items sold and total revenue generated."""
        total_sold = sum(s["quantity_sold"] for s in self.sales)
        total_revenue = round(sum(s["total_amount"] for s in self.sales), 2)
        return {
            "total_products_sold": total_sold,
            "total_revenue": total_revenue,
        }

    def sales_report(self):
        """Return a dict with total sales, revenue, and best-selling product."""
        summary = self.sales_summary()

        product_totals = {}
        for sale in self.sales:
            key = sale["product_name"]
            product_totals[key] = product_totals.get(key, 0) + sale["quantity_sold"]

        most_sold_product = None
        if product_totals:
            most_sold_product = max(product_totals, key=product_totals.get)

        return {
            "total_sales_transactions": len(self.sales),
            "total_products_sold": summary["total_products_sold"],
            "total_revenue": summary["total_revenue"],
            "most_sold_product": most_sold_product,
        }
