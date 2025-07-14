import os
from datetime import datetime
import json
import config

class Admin:
    def __init__(self, catalog):
        self.catalog = catalog
        self.user_files = config.user_files
        self.users = self.load_users()

    def load_users(self):
        if not os.path.isfile(self.user_files):
            return {}
        with open(self.user_files, 'r') as f:
            return json.load(f)

    def save_users(self):
        with open(self.user_files, 'w') as f:
            json.dump(self.users, f, indent=4)

    # Add Users to the System
    def add_users(self):
        print("\n\033[1;36m---------- 👥 Add New Users Page ----------\033[0m")
        username = input("\n\033[1mEnter Username: \033[0m").strip()
        if username in self.users:
            print("\n\033[31m ❌ Username already exists!\033[0m\n")
            return

        password = input("\033[1mEnter Password: \033[0m").strip()
        print("\n\033[1mPlease Select the User Role:\033[0m")
        print("\t1. Admin")
        print("\t2. User")
        role_input = input("\n\033[1mEnter Role Number : \033[0m").strip().lower()

        if role_input == "1":
            role = "admin"
        elif role_input == "2":
            role = "user"
        else:
            print("\n\033[31m ❌ Invalid Role Selected. Only 'admin' or 'user' Allowed.\033[0m\n")
            return

        self.users[username] = {
            "role": role,
            "password": password,
            "registered_date": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        }
        self.save_users()
        print(f'\n\033[34m ✅ User {username} with "{role}" role has been added successfully!\033[0m\n')

    def view_registered_users(self):
        print("\n\033[1;36m---------- 📋 Registered Users Page ----------\033[0m\n")

        # Reload user data from file to ensure the latest info
        if os.path.exists(self.user_files):
            with open(self.user_files, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

        if not self.users:
            print("\n\033[31m ❌ No Users Found!\033[0m\n")
            return

        for username, details in self.users.items():
            reg_date = details.get("registered_date", "-")
            print(f'Username: {username}  |  Role: {details["role"]}  |  Registered Date: {reg_date} \n')

    def add_products(self):
        print("\n\033[1;36m---------- ➕ Add New Products ----------\033[0m\n")
        try:
            name = input("\033[1mEnter Product Name: \033[0m")
            # Check for Duplicate Product Names
            if any(product["name"].lower() == name.lower() for product in self.catalog):
                print("\n\033[31m ❌ Product Name already exists!\033[0m")
                return

            price = float(input("\033[1mEnter Product Price: \033[0m"))
            sizes = input("\033[1mEnter Product Sizes (comma-seperated): \033[0m").upper().split(',')

            size_stock = {}
            for size in sizes:
                size = size.strip()
                quantity = int(input(f'\033[1mEnter Product Quantity for size {size}: \033[0m'))
                size_stock[size] = quantity

            new_id = max([p["id"] for p in self.catalog]) + 1

            self.catalog.append({
                "id": new_id,
                "name": name,
                "price": price,
                "sizes": list(size_stock.keys()),
                "stock": size_stock
            })
            print(f'\n\033[34m ✅ Product "{name}" Added Successfully with ID {new_id}.\033[0m\n')
        except ValueError:
            print("\n\033[31m ❌ Invalid Input. Ensure price and quantities are only numbers.\033[0m\n")
        except Exception as e:
            print(f'\n\033[31m ❌ Error : {e}\033[0m')

        self.save_catalog()

    def edit_products(self):
        print("\n\033[1;36m---------- ✏️ Edit Products ----------\033[0m\n")
        try:
            product_id = int(input("Enter Product ID: "))
            product = next((p for p in self.catalog if p["id"] == product_id), None)
            if not product:
                print("\n\033[31m ❌ Product not found.\033[0m\n")
                return

            print(f'\033[32mEditing {product["name"]}...\n\033[0m')
            name = input(f"\033[1mName ({product['name']}): \033[0m") or product["name"]

            price_input = input(f"\033[1mPrice ({product["price"]}): \033[0m")
            price = float(price_input) if (price_input) else product["price"]

            sizes_input = input(f"\033[1mSizes (comma-seperated):\033[0m").lower() or product['sizes']
            sizes = [size.strip().upper() for size in sizes_input.split(',')] if sizes_input else product["sizes"]

            #stock_input = input(f"\033[1mQuantity ({product["stock"]}): \033[0m")
            #stock = int(stock_input) if (stock_input) else product["stock"]
            quantity_by_size = {}
            print("\033[1mEnter quantity for each size: \033[0m")
            for size in sizes:
                quantity = input(f"\033[1m Enter Product Quantity for size {size.upper()}: \033[0m")
                while not quantity.isdigit():
                    print("\n\033[31m ❌ Please enter valid number.\n\033[0m")
                    quantity = input(f"\033[1m Enter Product Quantity for size {size.upper()}: \033[0m")
                quantity_by_size[size] = int(quantity)

            product['sizes'] = sizes
            product['stock'] = quantity_by_size

            product.update({"name": name, "price": price, "sizes": sizes, "stock": quantity_by_size})
            print("\n\033[34m ✅ Product Updated Successfully.\033[0m\n")

        except ValueError:
            print("\n\033[31m ❌ Invalid number entered.\n\033[0m")
        except Exception as e:
            print(f'\033[31m ❌ Unexpected Error: {e}\033[0m')

        self.save_catalog()

    def delete_products(self):
        print("\n\033[1;36m---------- 🗑️ Delete Products ----------\033[0m\n")
        try:
            product_id = int(input("\033[1mEnter Product ID: \033[0m"))
            indx =next((i for i, product in enumerate(self.catalog) if product["id"] == product_id), None)
            if indx is None:
                print("\n\033[31m ❌ Product not found.\033[0m\n")
                return

            confirm = input(f'\n\033[1mAre you sure you want to delete "{self.catalog[indx]['name']}"? (Y/N): \033[0m'.lower())
            if confirm == 'y':
                removed = self.catalog.pop(indx)
                print(f'\n\033[34m✅ " {removed["name"]}" Deleted Successfully.\033[0m\n')
            else:
                print("\n\033[31mProduct delete Cancelled.\033[0m\n")
        except ValueError:
            print("\n\033[31m ❌ Invalid ID.\033[0m\n")
        except Exception as e:
            print(f'\033[31m ❌ Unexpected Error: {e}\033[0m')

        self.save_catalog()

    # Catalog Insights - for Admin users
    def view_catalog_insights(self):
        print("\n\033[1;36m---------- 📊 Catalog Insights Page ----------\033[0m")
        total_items = len(self.catalog)

        # Calculate total stock units
        total_stock = sum(
            sum(item['stock'].values()) if isinstance(item['stock'], dict) else item['stock']
            for item in self.catalog
        )

        # Calculate total inventory value = sum of (price * total quantity per product)
        total_value = sum(
            item['price'] * (sum(item['stock'].values()) if isinstance(item['stock'], dict) else item['stock'])
            for item in self.catalog
        )

        print(f'\n\033[1mTotal Products:  {total_items}\033[0m')
        print(f'\033[1mTotal Stock Units: {total_stock}\033[0m')
        print(f'\033[1mTotal Inventory Value: Ұ{total_value:,.2f}\033[0m\n')

    # Monitor Stock - for Admin User
    def monitor_stock(self):
        print("\n\033[1;36m---------- 📦 Monitor Stock Page ----------\033[0m\n")
        low_stock_threshold = 3

        for item in self.catalog:
            stock = item['stock']
            if isinstance(stock, dict):
                total_stock = sum(stock.values())
            else:
                total_stock = stock

            status = "\033[31m ⚠️ Low Stock!!!\033[0m" if total_stock <= low_stock_threshold else "\033[32m ✅ Enough Stock Available\033[0m"
            print(f"{item['name']} | Total Stock {total_stock} →  {status}")

    # Save Catalog
    def save_catalog(self):
        with open(config.catalog_file, "w") as f:
            json.dump(self.catalog, f, indent=4)