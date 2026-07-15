# 📦 Inventory Management System

A console-based **Inventory Management System** built in Python as part of the
**Infobharat Interns (IBI) Python Development Internship** task. The system
helps businesses manage products, track stock levels, record sales, and
generate simple business reports — all through an easy-to-use, menu-driven
interface.

---

## 📌 Project Overview

This project simulates a real-world inventory workflow: adding products to a
catalog, tracking how much stock is available, recording sales as they
happen, and producing summary reports for both inventory and sales. All data
is stored locally in JSON files so it persists between runs.

## 🎯 Objective

Build a Python application that demonstrates:
- Object-oriented programming (OOP) design
- File handling and persistent data storage
- Menu-driven user interaction
- Defensive error handling for real-world edge cases

## ✨ Features

**Product Management**
- Add new products (ID, name, category, price, quantity, supplier)
- View all products in a formatted table
- Search products by Product ID or Product Name
- Update product name, category, price, or quantity
- Delete products by Product ID

**Stock Management**
- Add stock to increase available quantity
- Automatically reduce stock when a sale is recorded
- Low Stock Alert — lists all products below 10 units

**Sales Management**
- Record a sale (Product ID + quantity sold)
- Automatically calculates total sale amount and updates stock
- Sales Summary — total items sold and total revenue

**Reporting**
- Inventory Report — total products, total categories, total stock
- Sales Report — total transactions, revenue, and best-selling product

**Robust Error Handling**
- Rejects empty/invalid input, duplicate Product IDs, negative prices or
  quantities, and sales that exceed available stock
- Clear ❌ / ✅ messages so the user always knows what happened

## 🛠️ Technologies Used

- **Language:** Python 3.x
- **Standard Libraries:** `json`, `os`, `datetime`, `sys`
- **Optional Library:** `tabulate` (for nicer tables — the app falls back to
  a built-in plain-text table if it isn't installed, so no extra install is
  required)

## 📁 Project Structure

```
InventoryManagementSystem/
│
├── main.py                    # Entry point – menu-driven console interface
├── README.md                  # Project documentation (this file)
│
├── inventory/                 # Core application package
│   ├── __init__.py
│   ├── storage.py              # JSON load/save helper functions
│   ├── product_manager.py      # Product + stock management logic
│   └── sales_manager.py        # Sales recording + reporting logic
│
└── data/                      # Persistent data storage (auto-created)
    ├── products.json            # Product catalog
    └── sales.json                # Sales transaction history
```

## ▶️ How to Run

1. **Install Python 3** (if not already installed) — https://www.python.org/downloads/

2. **(Optional) Install `tabulate`** for prettier tables:
   ```bash
   pip install tabulate
   ```
   The app works perfectly fine without this step too.

3. **Navigate to the project folder:**
   ```bash
   cd InventoryManagementSystem
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

5. **Use the on-screen menu** to add products, record sales, and view
   reports. Sample data is already included in `data/products.json` and
   `data/sales.json` so you can explore the features immediately.

## 🧾 Sample Menu

```
=============================================
 📦 INVENTORY MANAGEMENT SYSTEM
=============================================
1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Add Stock
7. Record Sale
8. Inventory Report
9. Sales Report
10. Low Stock Alert
11. Exit
=============================================
```

## 🧪 Sample Data

The project ships with a few sample products (mouse, keyboard, notebook,
desk lamp) and two sample sales records, so the reports and low-stock alert
have realistic data to display right away. Feel free to delete the contents
of `data/products.json` and `data/sales.json` (replacing them with `[]`) to
start from a clean slate.

## 📸 Sample Output

*(Add screenshots of your terminal session here after running the app —
e.g. the main menu, a product table, and a sales report.)*

## 🌱 Possible Extensions (Bonus Ideas)

- Add simple username/password authentication
- Build a GUI front-end with Tkinter
- Export reports to PDF
- Chart sales trends with matplotlib
- Swap JSON storage for a SQLite database
- Wrap the same logic in a Flask web app

## 🙌 Acknowledgement

Built as part of the **Infobharat Interns** Python Development Internship
Program.
