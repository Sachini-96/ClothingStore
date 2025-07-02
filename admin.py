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
        print("\n\033[1;36m---------- Add New Users Page ----------\033[0m")
        username = input("\n\033[1mEnter Username: \033[0m").strip()
        if username in self.users:
            print("\n\033[31mUsername already exists!")
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
            print("\n\033[31mInvalid Role Selected. Only 'admin' or 'user' Allowed.\033[0m")
            return

        self.users[username] = {
            "role": role,
            "password": password,
            "registered_date": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        }
        self.save_users()
        print(f'\n\033[34mUser {username} with "{role}" role has been added successfully!\033[0m')

    def view_registered_users(self):
        print("\n\033[1;36m---------- Registered Users Page ----------\033[0m\n")

        # Reload user data from file to ensure the latest info
        if os.path.exists(self.user_files):
            with open(self.user_files, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

        if not self.users:
            print("\n\033[31mNo Users Found!\033[0m\n")
            return

        for username, details in self.users.items():
            reg_date = details.get("registered_date", "-")
            print(f'Username: {username}  |  Role: {details["role"]}  |  Registered Date: {reg_date} ')

    def add_products(self):
        print("\n\033[1;36m---------- Add New Products ----------\033[0m\n")
        try:
            name = input("\033[1mEnter Product Name: \033[10")
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
            print(f'\n\033[34mProduct "{name}" Added Successfully with ID {new_id}.\033[0m\n')
        except ValueError:
            print("\n\033[31mInvalid Input. Ensure price and quantities are only numbers.\033[0m\n")
        except Exception as e:
            print(f'\n\033[31mError : {e}\033[0m')

    def edit_products(self):
        print("\n\033[1;36m---------- Edit Products ----------\033[0m\n")
        try:
            product_id = int(input("Enter Product ID: "))
            product = next((p for p in self.catalog if p["id"] == product_id), None)
            if not product:
                print("\n\033[31mProduct not found.\033[0m\n")
                return

            print(f'\033[32mEditing {product["name"]}...\n\033[0m')
            name = input(f'\033[1mName ({product['name']}): \033[0m') or product["name"]
            price_input = input(f'\033[1mPrice ({product["price"]}): \033[0m')
            price = float(price_input) if (price_input) else product["price"]
            sizes_input = input(f'\033[1mSizes (comma-seperated): \033[0m')
            sizes = [s.strip().upper() for s in sizes_input.split(',')] if sizes_input else product["sizes"]
            stock_input = input(f'\033[1mQuantity ({product["stock"]}): \033[0m')
            stock = int(stock_input) if (stock_input) else product["stock"]

            product.update({"name": name, "price": price, "sizes": sizes, "stock": stock})
            print("\n\033[34mProduct Updated Successfully.\033[0m\n")

        except ValueError:
            print("\n\033[31mInvalid number entered.\n\033[0m")
        except Exception as e:
            print(f'\033[31mUnexpected Error: {e}\033[0m')

    def delete_products(self):
        print("\n\033[1;36m---------- Delete Products ----------\033[0m\n")
        try:
            product_id = int(input("\033[1mEnter Product ID: \033[0m"))
            indx =next((i for i, product in enumerate(self.catalog) if product["id"] == product_id), None)
            if indx is None:
                print("\n\033[31mProduct not found.\033[0m\n")
                return

            confirm = input(f'\n\033[1mAre you sure you want to delete "{self.catalog[indx]['name']}"? (Y/N): \033[0m'.lower())
            if confirm == 'y':
                removed = self.catalog.pop(indx)
                print(f'\033[34m"{removed["name"]}" Deleted Successfully.\033[0m\n')
            else:
                print("\n\033[31mProduct delete Cancelled.\033[0m\n")
        except ValueError:
            print("\n\033[31mInvalid ID.\033[0m\n")
        except Exception as e:
            print(f'\033[31mUnexpected Error: {e}\033[0m')

    # Catalog Insights - for Admin users
    def view_catalog_insights(self):
        print("\n\033[1;36m---------- Catalog Insights Page ----------\033[0m\n")
        total_items = len(self.catalog)
        total_stock = sum(item['stock'] for item in self.catalog)
        total_value = sum(item['stock'] * item['price'] for item in self.catalog)

        print(f'\n\033[1mTotal Products:  {total_items}\033[0m')
        print(f'\033[1mTotal Stock Units: {total_stock}\033[0m')
        print(f'\033[1mTotal Inventory Value: Ұ{total_value:.2f}\033[0m\n')

    # Monitor Stock - for Admin User
    def monitor_stock(self):
        print("\n\033[1;36m---------- Monitor Stock Page ----------\033[0m\n")
        low_stock_threshold = 3

        for item in self.catalog:
            status = "\033[31mLow Stock!!!\033[0m" if item['stock'] <= low_stock_threshold else "\033[32mEnough Stock Available\033[0m"
            print(f"{item['name']} | Stock {item['stock']} →  {status}")
