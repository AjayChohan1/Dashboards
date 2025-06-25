import sqlite3
from datetime import date


def connect():
    return sqlite3.connect('store.db')


def view_customers():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM Customers").fetchall()
        for row in rows:
            print(row)


def view_products():
    with connect() as conn:
        rows = conn.execute("SELECT * FROM Products").fetchall()
        for row in rows:
            print(row)


def add_product():
    name = input("Product name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    
    with connect() as conn:
        conn.execute(
            "INSERT INTO Products (name, price, stock) VALUES (?, ?, ?)",
            (name, price, stock)
        )
        print("Product added successfully.")


def place_order():
    customer_id = int(input("Customer ID: "))
    product_id = int(input("Product ID: "))
    quantity = int(input("Quantity: "))
    today = date.today()

    with connect() as conn:
        cursor = conn.cursor()
        
        # Insert into Orders table
        cursor.execute(
            "INSERT INTO Orders (customer_id, order_date) VALUES (?, ?)",
            (customer_id, today)
        )
        order_id = cursor.lastrowid

        # Insert into OrderItems
        cursor.execute(
            "INSERT INTO OrderItems (order_id, product_id, quantity) "
            "VALUES (?, ?, ?)",
            (order_id, product_id, quantity)
        )

        print(f"Order #{order_id} placed successfully.")


def view_orders():
    with connect() as conn:
        rows = conn.execute("""
            SELECT o.order_id, c.name, p.name, oi.quantity, o.order_date
            FROM Orders o
            JOIN Customers c ON o.customer_id = c.customer_id
            JOIN OrderItems oi ON o.order_id = oi.order_id
            JOIN Products p ON oi.product_id = p.product_id
            ORDER BY o.order_id;
        """).fetchall()
        for row in rows:
            print(row)


def menu():
    while True:
        print("\n==== Store Manager ====")
        print("1. View Customers")
        print("2. View Products")
        print("3. Add Product")
        print("4. Place Order")
        print("5. View Orders")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            view_customers()
        elif choice == '2':
            view_products()
        elif choice == '3':
            add_product()
        elif choice == '4':
            place_order()
        elif choice == '5':
            view_orders()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    menu()
