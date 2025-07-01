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
        print("\n\033[1;36m---------- Add New Users Page ----------\033[0m\n")
        username = input("\nEnter Username: ").strip()
        if username in self.users:
            print("\nUsername already exists!\n")
            return

        password = input("Enter Password: ").strip()
        print("\nPlease Select the User Role:")
        print("\t1. Admin")
        print("\t2. User")
        role_input = input("Enter Role Number : ").strip().lower()

        if role_input == "1":
            role = "admin"
        elif role_input == "2":
            role = "user"
        else:
            print("\nInvalid Role Selected. Only 'admin' or 'user' Allowed.")
            return

        self.users[username] = {
            "role": role,
            "password": password,
            "registered_date": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        }
        self.save_users()
        print(f'\nUser {username} with "{role}" role has been added successfully!')

    def view_registered_users(self):
        print("\n\033[1;36m---------- Registered Users Page ----------\033[0m\n")

        # Reload user data from file to ensure the latest info
        if os.path.exists(self.user_files):
            with open(self.user_files, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}

        if not self.users:
            print("\nNo Users Found!\n")
            return

        for username, details in self.users.items():
            reg_date = details.get("registered_date", "-")
            print(f'Username: {username}  |  Role: {details["role"]}  |  Registered Date: {reg_date} ')

    def add_products(self):
        print("\n\033[1;36m---------- Add New Products ----------\033[0m\n")
        try:
            name = input("Enter Product Name: ")
            price = input("Enter Product Price: ")
            sizes = input("Enter Product Sizes (comma-seperated): ").upper().split(',')

            size_stock = {}
            for size in sizes:
                size = size.strip()
                quantity = int(input(f'Enter Product Quantity for size {size}: '))
                size_stock[size] = quantity

            new_id = max([p["id"] for p in self.catalog]) + 1

            self.catalog.append({
                "id": new_id,
                "name": name,
                "price": price,
                "sizes": list(size_stock.keys()),
                "stock": size_stock
            })
            print(f'\nProduct "{name}" Added Successfully with ID {new_id}.\n')
        except ValueError:
            print("\nInvalid Input. Ensure price is a number and stock is an integer.\n")
        except Exception as e:
            print(f'Error : {e}')

    def edit_products(self):
        print("\n\033[1;36m---------- Edit Products ----------\033[0m\n")
        try:
            product_id = int(input("Enter Product ID: "))
            product = next((p for p in self.catalog if p["id"] == product_id), None)
            if not product:
                print("\nProduct not found.\n")
                return

            print(f'Editing {product["name"]}...\n')
            name = input(f'Name ({product['name']}): ') or product["name"]
            price_input = input(f'Price ({product["price"]}): ')
            price = float(price_input) if (price_input) else product["price"]
            sizes_input = input(f'Sizes (comma-seperated): ')
            sizes = [s.strip().upper() for s in sizes_input.split(',')] if sizes_input else product["sizes"]
            stock_input = input(f'Stock ({product["stock"]}): ')
            stock = int(stock_input) if (stock_input) else product["stock"]

            product.update({"name": name, "price": price, "sizes": sizes, "stock": stock})
            print("\nProduct Updated Successfully.\n")

        except ValueError:
            print("\nInvalid number entered.\n")
        except Exception as e:
            print(f'Unexpected Error: {e}')

    def delete_products(self):
        print("\n\033[1;36m---------- Delete Products ----------\033[0m\n")
        try:
            product_id = int(input("Enter Product ID: "))
            indx =next((i for i, product in enumerate(self.catalog) if product["id"] == product_id), None)
            if indx is None:
                print("\nProduct not found.\n")
                return

            confirm = input(f'Are you sure you want to delete "{self.catalog[indx]['name']}"? (Y/N):'.lower())
            if confirm == 'y':
                removed = self.catalog.pop(indx)
                print(f'"{removed["name"]}" Deleted Successfully.\n"')
            else:
                print("\nProduct delete Cancelled.\n")
        except ValueError:
            print("\nInvalid ID.\n")
        except Exception as e:
            print(f'Unexpected Error: {e}')

    # Catalog Insights - for Admin users
    def view_catalog_insights(self):
        print("\n\033[1;36m---------- Catalog Insights Page ----------\033[0m\n")
        total_items = len(self.catalog)
        total_stock = sum(item['stock'] for item in self.catalog)
        total_value = sum(item['stock'] * item['price'] for item in self.catalog)

        print(f'\nTotal Products:  {total_items}')
        print(f'Total Stock Units: {total_stock}')
        print(f'Total Inventory Value: Ұ{total_value:.2f}')

    # Monitor Stock - for Admin User
    def monitor_stock(self):
        print("\n\033[1;36m---------- Monitor Stock Page ----------\033[0m\n")
        low_stock_threshold = 3

        for item in self.catalog:
            status = "Low Stock!!!" if item['stock'] <= low_stock_threshold else "Enough Stock Available"
            print(f'{item['name']} | Stock {item['stock']} →  {status}')
