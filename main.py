from services.sales_manager import SalesManager
from analytics.sales_analyzer import SalesAnalyzer


sales_manager = SalesManager()
sales_analyzer = SalesAnalyzer()


while True:

    print("\n========================================")
    print("       CAFE MANAGEMENT SYSTEM")
    print("========================================")

    print("\n--- PRODUCT MANAGEMENT ---")
    print("1. Add Product")
    print("2. View Products")
    print("3. Update Product")
    print("4. Delete Product")

    print("\n--- CUSTOMER MANAGEMENT ---")
    print("5. Add Customer")
    print("6. View Customers")
    print("7. Update Customer")
    print("8. Delete Customer")

    print("\n--- USER MANAGEMENT ---")
    print("9. Add User")
    print("10. View Users")
    print("11. Update User")
    print("12. Delete User")

    print("\n--- ORDER MANAGEMENT ---")
    print("13. Create Order")
    print("14. View Orders")
    print("15. Update Order Status")
    print("16. Cancel Order")

    print("\n--- SALES ANALYTICS ---")
    print("17. View Sales Analytics")

    print("\n18. Exit")

    choice = input("\nEnter your choice: ")


    # =========================================================
    # PRODUCT - CREATE
    # =========================================================

    if choice == "1":

        product_name = input("Enter product name: ")
        category = input("Enter category: ")

        try:
            price = float(input("Enter price: "))
        except ValueError:
            print("Invalid price!")
            continue

        sales_manager.add_product(
            product_name,
            category,
            price,
            True
        )


    # =========================================================
    # PRODUCT - READ
    # =========================================================

    elif choice == "2":

        products = sales_manager.get_all_products()

        print("\n----------- PRODUCTS -----------")

        for product in products:
            print(product.get_details())


    # =========================================================
    # PRODUCT - UPDATE
    # =========================================================

    elif choice == "3":

        try:
            product_id = int(input("Enter product ID: "))
            price = float(input("Enter new price: "))
        except ValueError:
            print("Invalid input!")
            continue

        product_name = input("Enter new product name: ")
        category = input("Enter new category: ")

        availability_input = input(
            "Is product available? (yes/no): "
        )

        availability = (
            availability_input.lower() == "yes"
        )

        sales_manager.update_product(
            product_id,
            product_name,
            category,
            price,
            availability
        )


    # =========================================================
    # PRODUCT - DELETE
    # =========================================================

    elif choice == "4":

        try:
            product_id = int(
                input("Enter product ID to delete: ")
            )
        except ValueError:
            print("Invalid product ID!")
            continue

        sales_manager.delete_product(product_id)


    # =========================================================
    # CUSTOMER - CREATE
    # =========================================================

    elif choice == "5":

        name = input("Enter customer name: ")
        phone = input("Enter customer phone: ")

        sales_manager.add_customer(
            name,
            phone
        )


    # =========================================================
    # CUSTOMER - READ
    # =========================================================

    elif choice == "6":

        customers = sales_manager.get_all_customers()

        print("\n----------- CUSTOMERS -----------")

        for customer in customers:
            print(customer.get_details())


    # =========================================================
    # CUSTOMER - UPDATE
    # =========================================================

    elif choice == "7":

        try:
            customer_id = int(
                input("Enter customer ID: ")
            )
        except ValueError:
            print("Invalid customer ID!")
            continue

        name = input("Enter new customer name: ")
        phone = input("Enter new customer phone: ")

        sales_manager.update_customer(
            customer_id,
            name,
            phone
        )


    # =========================================================
    # CUSTOMER - DELETE
    # =========================================================

    elif choice == "8":

        try:
            customer_id = int(
                input("Enter customer ID to delete: ")
            )
        except ValueError:
            print("Invalid customer ID!")
            continue

        sales_manager.delete_customer(customer_id)


    # =========================================================
    # USER - CREATE
    # =========================================================

    elif choice == "9":

        name = input("Enter user name: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = input(
            "Enter role (Staff/Admin/Owner): "
        )

        sales_manager.add_user(
            name,
            username,
            password,
            role
        )


    # =========================================================
    # USER - READ
    # =========================================================

    elif choice == "10":

        users = sales_manager.get_all_users()

        print("\n----------- USERS -----------")

        for user in users:
            print(user.get_details())


    # =========================================================
    # USER - UPDATE
    # =========================================================

    elif choice == "11":

        try:
            user_id = int(
                input("Enter user ID: ")
            )
        except ValueError:
            print("Invalid user ID!")
            continue

        name = input("Enter new name: ")
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        role = input(
            "Enter new role (Staff/Admin/Owner): "
        )

        sales_manager.update_user(
            user_id,
            name,
            username,
            password,
            role
        )


    # =========================================================
    # USER - DELETE
    # =========================================================

    elif choice == "12":

        try:
            user_id = int(
                input("Enter user ID to delete: ")
            )
        except ValueError:
            print("Invalid user ID!")
            continue

        sales_manager.delete_user(user_id)


    # =========================================================
    # ORDER - CREATE
    # =========================================================

    elif choice == "13":

        try:
            customer_id = int(
                input("Enter customer ID: ")
            )

            user_id = int(
                input("Enter staff/user ID: ")
            )

        except ValueError:
            print("Invalid customer ID or user ID!")
            continue

        items = []

        while True:

            try:
                product_id = int(
                    input("Enter product ID: ")
                )

                quantity = int(
                    input("Enter quantity: ")
                )

            except ValueError:
                print("Invalid product ID or quantity!")
                continue

            items.append(
                (product_id, quantity)
            )

            more = input(
                "Add another product? (yes/no): "
            )

            if more.lower() != "yes":
                break

        sales_manager.create_order(
            customer_id,
            user_id,
            items
        )


    # =========================================================
    # ORDER - READ
    # =========================================================

    elif choice == "14":

        orders = sales_manager.get_all_orders()

        print("\n----------- ORDERS -----------")

        for order in orders:
            print(order.get_details())


    # =========================================================
    # ORDER - UPDATE STATUS
    # =========================================================

    elif choice == "15":

        try:
            order_id = int(
                input("Enter order ID: ")
            )
        except ValueError:
            print("Invalid order ID!")
            continue

        print("\nAvailable statuses:")
        print("1. Pending")
        print("2. Preparing")
        print("3. Ready")
        print("4. Completed")
        print("5. Cancelled")

        status_choice = input(
            "Select status: "
        )

        status_map = {
            "1": "Pending",
            "2": "Preparing",
            "3": "Ready",
            "4": "Completed",
            "5": "Cancelled"
        }

        status = status_map.get(status_choice)

        if status is None:
            print("Invalid status!")
            continue

        sales_manager.update_order_status(
            order_id,
            status
        )


    # =========================================================
    # ORDER - CANCEL
    # =========================================================

    elif choice == "16":

        try:
            order_id = int(
                input("Enter order ID to cancel: ")
            )
        except ValueError:
            print("Invalid order ID!")
            continue

        sales_manager.cancel_order(
            order_id
        )


    # =========================================================
    # SALES ANALYTICS
    # =========================================================

    elif choice == "17":

        sales_data = sales_analyzer.get_sales_data()

        if sales_data.empty:
            print("\nNo completed sales available.")
            continue


        # -----------------------------------------------------
        # Total Revenue
        # -----------------------------------------------------

        total_revenue = (
            sales_analyzer.get_total_revenue(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Total Orders
        # -----------------------------------------------------

        total_orders = (
            sales_analyzer.get_total_orders(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Average Order Value
        # -----------------------------------------------------

        average_order_value = (
            sales_analyzer.get_average_order_value(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Best Selling Product
        # -----------------------------------------------------

        best_product, quantity_sold = (
            sales_analyzer.get_best_selling_product(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Category Analysis
        # -----------------------------------------------------

        category_analysis = (
            sales_analyzer.get_category_analysis(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Peak Sales Time
        # -----------------------------------------------------

        peak_hour, peak_quantity = (
            sales_analyzer.get_peak_sales_time(
                sales_data
            )
        )


        # -----------------------------------------------------
        # Business Insights
        # -----------------------------------------------------

        insights = (
            sales_analyzer.generate_business_insights(
                sales_data
            )
        )


        # =====================================================
        # DISPLAY ANALYTICS
        # =====================================================

        print("\n========================================")
        print("          SALES ANALYTICS")
        print("========================================")


        print("\n--- SALES KPIs ---")

        print(
            f"Total Revenue       : Rs. {total_revenue:.2f}"
        )

        print(
            f"Total Orders        : {total_orders}"
        )

        print(
            f"Average Order Value : Rs. {average_order_value:.2f}"
        )

        print(
            f"Best Selling Product: {best_product}"
        )

        print(
            f"Quantity Sold       : {quantity_sold}"
        )


        print("\n--- CATEGORY ANALYSIS ---")

        print(category_analysis)


        print("\n--- PEAK SALES TIME ---")

        print(
            f"Peak Sales Hour : {peak_hour}:00"
        )

        print(
            f"Quantity Sold   : {peak_quantity}"
        )


        print("\n--- BUSINESS INSIGHTS ---")

        for insight in insights:
            print(f"• {insight}")


    # =========================================================
    # EXIT
    # =========================================================

    elif choice == "18":

        print("\nProgram closed.")
        break


    # =========================================================
    # INVALID CHOICE
    # =========================================================

    else:

        print("\nInvalid choice. Please try again.")
        