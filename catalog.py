from datetime import datetime
from itertools import product

from config import catalog_file
import json
import os
import config

class Catalog():

    def __init__(self, store_instance):
        self.store = store_instance
        self.catalog_file = catalog_file
        self.catalog = self.load_catalog()
        self.purchase_history = config.purchase_history_file

    # Load Catalog
    def load_catalog(self):
        if not os.path.exists(self.catalog_file):
            # Create default catalog
            default_catalog = [
                {"id": 1, "name": "T-Shirt", "price": 2500.00, "sizes": ["S", "M", "L"], "stock": {"S": 3, "M": 4, "L": 3}},
                {"id": 2, "name": "Jeans", "price": 4890.00, "sizes": ["M", "L", "XL"], "stock": {"M": 2, "L": 2, "XL": 1}},
                 {"id": 3, "name": "Jacket", "price": 7600.00, "sizes": ["M", "L"], "stock": {"M": 1, "L": 2}},
            ]
            with open(catalog_file, "w") as f:
                json.dump(default_catalog, f, indent=4)
            return default_catalog
        else:
            with open(self.catalog_file, "r") as f:
                return json.load(f)

    # Save Data to Catalog
    def save_catalog(self):
        with open(self.catalog_file, "w") as f:
            json.dump(self.catalog, f, indent=4)

    # View Catalog
    def view_catalog(self):
        print("\n\033[1;95m-------------------- 🧾 Catalog --------------------\033[0m\n")

        # Print header
        print(f"\033[1m{'ID':<5} {'Name':<10} {'Price (Ұ)':<12} {'Sizes':<15} {'Stock':<6}\033[0m")
        print("-" * 50)

        for item in self.catalog:
            sizes = ", ".join(item['sizes'])

            stock_value = item['stock']
            if isinstance(stock_value, dict):
                total_stock = sum(stock_value.values())
            else:
                total_stock = stock_value

            print(f"{item['id']:<5} {item['name']:<10} Ұ{item['price']:<10,.2f} {sizes:<12} {total_stock:<6}")

        print("-" * 50)
        print("\n\t1. 🔍 Search Product")
        print("\t2. 🧃 Filter Products")
        print("\t3. ➕ Add to Cart")
        print("\t4. 🔙 Back to Menu")

        # Get user Selection
        user_choice = input("\n\033[1m 👉 Enter your choice: \033[0m")

        if user_choice == "1":
            self.search_product()
        elif user_choice == "2":
            self.filter_products()
        elif user_choice == "3":
            self.add_to_cart()
            checkout_now = input("\n🛒 Proceed to checkout now? (y/n): ").strip().lower()
            if checkout_now == 'y':
                self.checkout()
                return
            elif checkout_now == 'n':
                print("\n\033[33mCheckout cancelled. Returning to Catalog menu...\033[0m")
            else:
                print("\n\033[31mInvalid input. Returning to Catalog menu...\033[0m")
        elif user_choice == "4":
            return

    # Searching Products
    def search_product(self):
        print("\n\033[1;95m---------- 🔍 Search Product Page ----------\033[0m\n")
        keyword = input("\033[1mEnter keyword: \033[0m").lower()

        found = False
        for item in self.catalog:
            if keyword in item['name'].lower():
                print(f"\n{item['id']}: {item['name']} - Ұ{item['price']:,.2f} | Sizes: {', '.join(item['sizes'])} | Stock: {item['stock']}")
                found = True
        if not found:
            print("\n\033[31m ❌ No Matching Products Found...\033[0m")

        self.view_catalog()

    # Fitering Products by Size and Price
    def filter_products(self):
        while True:
            print("\n\033[1;95m---------- 🧃 Filter Products ----------\033[0m\n")
            print("\t1. 📏 Filter by Size")
            print("\t2. 💰 Filter by Price")
            print("\t3. 🔙 Back to Menu")

            user_filter_option = input("\n\033[1m 👉 Enter your choice: \033[0m")

            # Filter Products by Size
            if user_filter_option == "1":
                print("\n\033[1;95m---------- Filter Products by Size ----------\033[0m")
                user_entered_size = input("\n\033[1mEnter the size for filter items: \033[0m").upper()
                print()

                found = False
                for item in self.catalog:
                    if user_entered_size in item['sizes']:
                        print(f"{item['id']}: {item['name']} - Ұ{item['price']:,.2f} | Sizes: {', '.join(item['sizes'])} | Stock: {item['stock']}")
                        found = True
                if not found:
                    print("\033[31m ❌ No products found for given size...\033[0m")

            # Filter Products by Price+
            elif user_filter_option == "2":
                print("\n\033[1;95m---------- Filter Products by Price ----------\033[0m")
                try:
                    user_entered_min_price = float(input("\n\033[1mEnter the Minimum price for filter items: \033[0m"))
                    user_entered_max_price =float(input("\033[1mEnter the Maximum price for filter items: \033[0m"))
                    print()

                    found = False
                    for item in self.catalog:
                        if user_entered_min_price <= item['price'] <= user_entered_max_price:
                            print(f"{item['id']}: {item['name']} - Ұ{item['price']:,.2f} | Sizes: {', '.join(item['sizes'])} | Stock: {item['stock']}")
                            found = True
                    if not found:
                        print("\n\033[31m ❌ No products found for given price...\033[0m")
                except ValueError:
                    print("\n\033[31m ❌ Invalid input. Please try again...\033[0m")

            # Back to User Menu
            elif user_filter_option == "3":
                return
            else:
                print("\n\033[31m ❌ Invalid Choice. Please try again...\033[0m")
                self.filter_products()


    # Add Items to the Cart
    def add_to_cart(self):
        print("\n\033[1;95m----------  ➕ Add to cart  ----------\033[0m")
        try:
            selected_item_id = int(input("\n\033[1mEnter ID of the item you want to add: \033[0m"))

            product = next((item for item in self.catalog if item['id'] == selected_item_id), None)

            if not product:
                print("\n\033[31m ❌ No product found for given ID...\033[0m")
                return

            print(f"Available Sizes: {', '.join(product['sizes'])}")
            selected_size = input("\n\033[1mEnter Size: \033[0m").strip().upper()

            if not isinstance(product['stock'], dict):
                print("\n\033[31m ❌ Error: Stock format invalid for this product!\033[0m")
                return

            if selected_size not in product['stock']:
                print("\n\033[31m ❌ Selected size is not available in stock!\033[0m")
                return

            available_stock = product['stock'].get(selected_size, 0)
            quantity = int(input("\033[1mEnter quantity: \033[0m"))

            if quantity > available_stock:
                print("\n\033[31m ❌ Sorry! Requested quantity exceeds available stock.\033[0m")
                return

            #product['stock'][selected_size] -= quantity

            self.store.cart[(selected_item_id, selected_size)] = {
                'quantity': quantity,
                'product': product,
                'size': selected_size
            }

            print(
                f'\n\033[34m ✅ Successfully added {quantity} x {product["name"]} (Size {selected_size}) to cart.\033[0m')

        except ValueError:
            print("\n\033[31m ❌ Invalid input. Please try again...\033[0m")

    # View Cart
    def view_cart(self):
        print("\n\033[1;95m---------- 🛒 Your Cart ----------\033[0m\n")
        if not self.store.cart:
            print("\n\033[31m ❌ Your Cart is empty. Add some items first!\033[0m")
            return

        total_value = 0
        print("\033[1mItems in your cart: \033[0m")

        for item_id, cart_item in self.store.cart.items():
            product = cart_item['product']
            quantity = cart_item['quantity']
            price = product['price']
            subtotal = price * quantity
            total_value += subtotal
            print(f"{product['name']} x {quantity} = Ұ{subtotal:,.2f}")

        print(f'\n\033[32mYour Total Amount : Ұ{total_value:.2f}\033[0m')

        proceed_to_checkout = input("\n\033[1mProceed to checkout? (y/n): \033[0m").strip().lower()

        if proceed_to_checkout == "y":
            self.checkout()
            return
        elif proceed_to_checkout == "n":
            print("\n\033[33mCheckout Cancelled... \033[0m")
            return
        else:
            print("\n\033[31m Invalid input. Please enter 'y' or 'n'.\033[0m")


    # Checkout
    def checkout(self):
        print("\n\033[1;95m---------- Checkout Page ----------\033[0m\n")
        if not self.store.cart:
            print("\n\033[31m ❌ Your Cart is empty. Add some items first!\033[0m")
            return

        for(item_id, size), cart_item in list(self.store.cart.items()):
            # Deduct from the Stock
            product = cart_item['product']
            quantity = cart_item['quantity']

            if isinstance(product['stock'], dict):
                if size in product['stock']:
                    product['stock'][size] -= quantity
                else:
                    print(f"\n\033[31m ❌ Error: Size {size} is notfound in stock!\033[0m")
            else:
                product['stock'] -= quantity

            #Save to History
            self.save_purchase_history(self.store.cart)

            self.store.cart.clear()
            print("\n\033[34m ✅ Your Order Successful! Thank you for your purchase.\033[0m")

    def save_purchase_history(self, cart):
        history = []

        if os.path.exists(self.purchase_history):
            with open(self.purchase_history, 'r') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    pass

        # Build new History Record
        new_record = {
            "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
            "type": 'purchase',
            "items":[
                {
                    "name": item['product']['name'],
                    "price": item['product']['price'],
                    "quantity": item['quantity'],
                    "size": item['size']
                } for item in cart.values()
            ]
        }
        history.append(new_record)

        with open(self.purchase_history, 'w') as f:
            json.dump(history, f, indent=4)

    # View Purchase History
    def view_purchase_history(self):
        print("\n\033[1;95m---------- 🕓 Purchase History ----------\033[0m\n")

        if not os.path.exists(self.purchase_history):
            print("\033[31m ❌ No Purchase History Found.\033[0m")
            return

        with open(self.purchase_history, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                print("\033[31m ❌ Error reading Purchase History.\033[0m")
                return

        if not history:
            print("\033[31m ❌ No Purchase History Found.\033[0m")
            return

        for record in history:
            label = record.get("type", "purchase").capitalize()
            print(f"{label} - Date: {record['timestamp']}")
            for item in record['items']:
                print(f" - {item['name']} x {item['quantity']} @ Ұ{item['price']:,.2f}")
            print()

    # Return Items
    def return_items(self):
        print("\n\033[1;95m---------- 🔁 Return Items ----------\n\033[0m")

        if not os.path.exists(self.purchase_history):
            print("\033[31m ❌ No Purchase History Found.\033[0m")
            return

        # Load History
        try:
            with open(self.purchase_history, 'r') as f:
                history = json.load(f)
        except json.JSONDecodeError:
            print("\033[31m ❌ Error reading Purchase History.\033[0m")
            return

        if not history:
            print("\033[31m ❌ No Purchases to Return.\033[0m")
            return

        # Show Available Purchases
        all_items = []
        print("\033[1mYour Purchase History: \n\033[0m")
        for i,record in enumerate(history):
            print(f"{i + 1}. Date : {record['timestamp']}")
            for j,item in enumerate(record['items']):
                index = len(all_items)
                #Record index + item
                all_items.append((i, item))
                print(f" [{index}] {item['name']} x {item['quantity']} @ Ұ{item['price']:,.2f}")
        print()

        # Select Item to Return
        try:
            return_index = int(input("\033[1mWhich item do you want to return: \033[0m"))
        except ValueError:
            print("\n\033[31m ❌ Please enter a valid selection.\033[0m")
            return

        if return_index < 0 or return_index >= len(all_items):
                print("\n\033[31m ❌ Invalid Selection. Please choose a valid item number.\033[0m")
                return

        record_index, item_to_return = all_items[return_index]
        item_name = item_to_return['name']
        item_quantity = item_to_return['quantity']
        item_size = item_to_return.get('size', None)

        # Ask Return Quantity
        try:
            return_quantity = int(input("\033[1mHow many items do you want to return: \033[0m"))
            if return_quantity < 0 or return_quantity > item_quantity:
                print("\n\033[31m ❌ Invalid Quantity\033[0m")
                return
        except ValueError:
            print("\n\033[31m ❌ Please enter a valid number.\033[0m")
            return

        # Update Stock
        for product in self.catalog:
            if product['name'] == item_name:
                if isinstance(product['stock'], dict) and item_size in product['stock']:
                    product['stock'][item_size] += return_quantity
                else:
                    #product['stock'] += return_quantity
                    print("\n\033[31m ❌ Size mismatch or stock format invalid.\033[0m")
                    return
                break
            else:
                # This executes only if for loop complete without break
                print("\n\033[31m ❌ Returned item not found in catalog.\033[0m")
                return

        # Adjust Purchase Record
        if return_quantity == item_quantity:
            history[record_index]['items'].remove(item_to_return)
        else:
            item_to_return['quantity'] -= return_quantity

        # Check whether the order has any other items
        if not history[record_index]['items']:
            # Remove Record if no other items
            del history[record_index]

        # Save Updated History
        with open(self.purchase_history, 'w') as f:
            json.dump(history, f, indent=4)

        print(f'\n\033[34m ✅ Successfully Returned {return_quantity} x {item_name}.\033[0m')

    def save_return_history(self,item_name, return_quantity, price):
        history = []

        if not os.path.exists(self.purchase_history):
            with open(self.purchase_history, 'w') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    pass

        return_record = {
            "timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
            "type": "return",
            "items": [
                {
                    "name": item_name,
                    "price": price,
                    "quantity": return_quantity
                }
            ]
        }

        history.append(return_record)

        with open(self.purchase_history, 'w') as f:
            json.dump(history, f, indent=4)

if __name__ == "__main__":
    from store import Store
    store = Store()
    store.catalog.view_catalog()