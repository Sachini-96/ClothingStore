import json
import os
import config
from catalog import Catalog
from admin import Admin
from datetime import datetime


class Store():

    def __init__(self):
        self.user_file = config.user_files
        self.users = self.load_users()
        self.current_user = None

        self.cart = {}
        self.catalog = Catalog(self)
        self.admin = Admin(self.catalog.catalog)

    def load_users(self):
        if not os.path.exists(self.user_file):
            # Create default admin user
            default_admin_user = {
                "admin": {
                    "password": "123",
                    "role": "admin",
                }
            }
            with open(self.user_file, 'w') as f:
                json.dump(default_admin_user, f, indent=4)
            return default_admin_user

        with open(self.user_file, 'r') as f:
            return json.load(f)

    def save_users(self):
        with open(self.user_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    # Login Function
    def login(self):
        print("\n\033[1;95m---------- Login Page ----------\033[0m")
        username = input("\n\033[1mPlease enter your Username: \033[0m")
        password = input("\033[1mPlease enter your Password: \033[0m")

        user = self.users.get(username)
        if user and user['password'] == password:
            print(f'\n\033[34mWelcome {username}! You are now logged in.\033[0m')
            self.current_user = {"username": username, "role": user['role']}
            self.user_menu()
        else:
            print("\n\033[31mInvalid Username or Password. Please try again!\033[0m")

    # Register New User Function
    def register_new_user(self):
        print("\n\033[1;95m---------- Register Page ----------\033[0m")
        username = input("\n\033[1mEnter Username : \033[0m")

        if username in self.users:
            print("\n\033[31mUsername Already Exists.\033[0m")
            return

        password = input("\033[1;34mEnter Password: \033[0m")

        self.users[username] = {
            "password": password,
            "role": "user", # When registering, default role is normal user
            "registered_date": datetime.now().strftime("%m/%d/%Y %I:%M%p")
        }
        self.save_users()

        print(f'\nUser "{username}" registered successfully.')
        self.login()

    # Exit from the Page Function
    def exit_page(self):
        print("\n\033[33mExiting from the System...\033[0m")
        exit()

    # Display Main Menu
    def main_menu(self):
        print("\n\033[1;95m==========  🛍️ Welcome to the Sakura Clothing Store 🛍️  ️==========\033[0m")
        print("\n\033[1mPlease select from the following options:\033[0m")
        print("\t1. Login")
        print("\t2. Register")
        print("\t3. Exit")

        # Get User Choice
        choice = input("\n\033[1m 👉 Enter your choice: \033[0m")
        if choice == "1":
            self.login()
        elif choice == "2":
            self.register_new_user()
        elif choice == "3":
            self.exit_page()
        else:
            print("\n\033[31mSorry, invalid option. Please try again.\033[0m")
            self.main_menu()

    # Display User Menu After Logged in
    def user_menu(self):
        role = self.current_user['role']

        print(f'\n\033[1;95m---------- {role.title()} Menu Page ----------\033[0m\n')
        if role == "user":
            print("\t1. 🧾 View Catalog")
            print("\t2. 🕓 Purchase History")
            print("\t3. 🛒 View Cart")
            print("\t4. 🔁 Return Item")
            print("\t5. 🚪 Logout")

            # Get User Choice
            choice = input("\n\033[1m 👉 Enter your choice: \033[0m")
            if choice == "1":
                self.catalog.view_catalog()
                # After Viewing Catalog, Return back to User Menu
                self.user_menu()
            elif choice == "2":
                self.catalog.view_purchase_history()
                # After Save details to purchase history, Return back to the User Menu
                self.user_menu()
            elif choice == "3":
                self.catalog.view_cart()
            elif choice == "4":
                self.catalog.return_items()
                # After Returning Items, Return back to the User Menu
                self.user_menu()
            elif choice == "5":
                print("\n\033[33m👋 Logging out... \nReturning to Main Menu...\033[0m")
                self.main_menu()
            else:
                print("\n\033[31m❌ Sorry, invalid option. Please try again.\033[0m")
            self.user_menu()

        elif role == "admin":
            while True:
                print("1. Add Users")
                print("2. View User Details")
                print("3. Add Product")
                print("4. Edit Catalog")
                print("5. Delete Catalog")
                print("6. View Catalog")
                print("7. View Catalog Insight")
                print("8. Monitor Stock")
                print("9. Logout")

                admin_choice = input("\n\033[1m 👉 Enter your choice: \033[0m")
                if admin_choice == "1":
                    self.admin.add_users()
                elif admin_choice == "2":
                    self.admin.view_registered_users()
                elif admin_choice == "3":
                    self.admin.add_products()
                elif admin_choice == "4":
                    self.admin.edit_products()
                elif admin_choice == "5":
                    self.admin.delete_products()
                elif admin_choice == "6":
                    self.catalog.view_catalog()
                elif admin_choice == "7":
                    self.admin.view_catalog_insights()
                elif admin_choice == "8":
                    self.admin.monitor_stock()
                elif admin_choice == "9":
                    print("\n\033[33m👋 Logging out... \nReturning to Main Menu...\033[0m")
                    self.main_menu()
                else:
                    print("\n\033[31m❌ Sorry, invalid option. Please try again.\033[0m")
                self.user_menu()

if __name__ == "__main__":
        app = Store()
        app.main_menu()