from datetime import datetime

from mysql.connector import IntegrityError

from database.connection import get_connection
from models.product import Product
from models.customer import Customer
from models.user import User
from models.order import Order
from models.order_item import OrderItem
from models.cafe_table import CafeTable


class SalesManager:

    # =========================================================
    # PRODUCT - READ
    # =========================================================

    def get_all_products(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    product_id,
                    product_name,
                    category,
                    price,
                    availability,
                    image_url
                FROM product
                ORDER BY product_id
                """
            )

            rows = cursor.fetchall()

            products = []

            for row in rows:

                product = Product(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )

                products.append(product)

            return products

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # PRODUCT - CREATE
    # =========================================================

    def add_product(
        self,
        product_name,
        category,
        price,
        availability=True,
        image_url=None
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO product
            (
                product_name,
                category,
                price,
                availability,
                image_url
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            product_name,
            category,
            price,
            availability,
            image_url
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            product_id = cursor.lastrowid

            print(
                "Product added successfully!"
            )

            return (
                True,
                product_id
            )

        except IntegrityError as error:

            connection.rollback()

            print(
                "Could not add product."
            )

            print(error)

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # PRODUCT - UPDATE
    # =========================================================

    def update_product(
        self,
        product_id,
        product_name,
        category,
        price,
        availability,
        image_url=None
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE product
            SET
                product_name = %s,
                category = %s,
                price = %s,
                availability = %s,
                image_url = %s
            WHERE product_id = %s
        """

        values = (
            product_name,
            category,
            price,
            availability,
            image_url,
            product_id
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "Product updated successfully!"
                )

                return (
                    True,
                    "Product updated successfully."
                )

            print(
                "Product not found!"
            )

            return (
                False,
                "Product not found."
            )

        except IntegrityError as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # PRODUCT - DELETE
    # =========================================================

    def delete_product(self, product_id):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM product
            WHERE product_id = %s
        """

        values = (
            product_id,
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "Product deleted successfully!"
                )

                return (
                    True,
                    "Product deleted successfully."
                )

            print(
                "Product not found!"
            )

            return (
                False,
                "Product not found."
            )

        except IntegrityError:

            connection.rollback()

            message = (
                "Cannot delete this product because "
                "it is used in existing orders."
            )

            print(message)

            return (
                False,
                message
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # CUSTOMER - READ
    # =========================================================

    def get_all_customers(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    customer_id,
                    name,
                    phone
                FROM customer
                ORDER BY customer_id
                """
            )

            rows = cursor.fetchall()

            customers = []

            for row in rows:

                customer = Customer(
                    row[0],
                    row[1],
                    row[2]
                )

                customers.append(customer)

            return customers

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # CUSTOMER - CREATE
    # =========================================================

    def add_customer(
        self,
        name,
        phone
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO customer
            (
                name,
                phone
            )
            VALUES (%s, %s)
        """

        values = (
            name,
            phone
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            customer_id = cursor.lastrowid

            print(
                "Customer added successfully!"
            )

            print(
                f"Customer ID: {customer_id}"
            )

            return (
                True,
                customer_id
            )

        except IntegrityError as error:

            connection.rollback()

            print(
                "Could not add customer."
            )

            print(error)

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # CUSTOMER - UPDATE
    # =========================================================

    def update_customer(
        self,
        customer_id,
        name,
        phone
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE customer
            SET
                name = %s,
                phone = %s
            WHERE customer_id = %s
        """

        values = (
            name,
            phone,
            customer_id
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "Customer updated successfully!"
                )

                return (
                    True,
                    "Customer updated successfully."
                )

            print(
                "Customer not found!"
            )

            return (
                False,
                "Customer not found."
            )

        except IntegrityError as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # CUSTOMER - DELETE
    # =========================================================

    def delete_customer(
        self,
        customer_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM customer
            WHERE customer_id = %s
        """

        values = (
            customer_id,
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "Customer deleted successfully!"
                )

                return (
                    True,
                    "Customer deleted successfully."
                )

            print(
                "Customer not found!"
            )

            return (
                False,
                "Customer not found."
            )

        except IntegrityError:

            connection.rollback()

            message = (
                "Cannot delete this customer because "
                "existing orders are linked to this customer."
            )

            print(message)

            return (
                False,
                message
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # TABLE - READ
    # =========================================================

    def get_all_tables(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    table_id,
                    table_number,
                    capacity,
                    status
                FROM cafe_table
                ORDER BY table_id
                """
            )

            rows = cursor.fetchall()

            tables = []

            for row in rows:

                table = CafeTable(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                )

                tables.append(table)

            return tables

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # TABLE - AVAILABLE TABLES
    # =========================================================

    def get_available_tables(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    table_id,
                    table_number,
                    capacity,
                    status
                FROM cafe_table
                WHERE status = 'Available'
                ORDER BY table_id
                """
            )

            rows = cursor.fetchall()

            tables = []

            for row in rows:

                table = CafeTable(
                    row[0],
                    row[1],
                    row[2],
                    row[3]
                )

                tables.append(table)

            return tables

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # TABLE - UPDATE STATUS
    # =========================================================

    def update_table_status(
        self,
        table_id,
        status
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE cafe_table
            SET status = %s
            WHERE table_id = %s
        """

        values = (
            status,
            table_id
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                message = (
                    "Table status updated successfully."
                )

                print(message)

                return (
                    True,
                    message
                )

            message = "Table not found."

            print(message)

            return (
                False,
                message
            )

        except IntegrityError as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # USER - READ
    # =========================================================

    def get_all_users(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    user_id,
                    name,
                    username,
                    password,
                    role
                FROM users
                ORDER BY user_id
                """
            )

            rows = cursor.fetchall()

            users = []

            for row in rows:

                user = User(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )

                users.append(user)

            return users

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # USER - CREATE
    # =========================================================

    def add_user(
        self,
        name,
        username,
        password,
        role
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO users
            (
                name,
                username,
                password,
                role
            )
            VALUES (%s, %s, %s, %s)
        """

        values = (
            name,
            username,
            password,
            role
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            user_id = cursor.lastrowid

            print(
                "User added successfully!"
            )

            return (
                True,
                user_id
            )

        except IntegrityError:

            connection.rollback()

            message = (
                "Username already exists. "
                "Please choose another username."
            )

            print(message)

            return (
                False,
                message
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # USER - UPDATE
    # =========================================================

    def update_user(
        self,
        user_id,
        name,
        username,
        password,
        role
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE users
            SET
                name = %s,
                username = %s,
                password = %s,
                role = %s
            WHERE user_id = %s
        """

        values = (
            name,
            username,
            password,
            role,
            user_id
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "User updated successfully!"
                )

                return (
                    True,
                    "User updated successfully."
                )

            print(
                "User not found!"
            )

            return (
                False,
                "User not found."
            )

        except IntegrityError:

            connection.rollback()

            message = (
                "Username already exists. "
                "Please choose another username."
            )

            return (
                False,
                message
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # USER - DELETE
    # =========================================================

    def delete_user(
        self,
        user_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            DELETE FROM users
            WHERE user_id = %s
        """

        values = (
            user_id,
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                print(
                    "User deleted successfully!"
                )

                return (
                    True,
                    "User deleted successfully."
                )

            print(
                "User not found!"
            )

            return (
                False,
                "User not found."
            )

        except IntegrityError:

            connection.rollback()

            message = (
                "Cannot delete this user because "
                "existing orders are linked to this user."
            )

            return (
                False,
                message
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - READ
    # =========================================================

    def get_all_orders(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    order_id,
                    customer_id,
                    user_id,
                    table_id,
                    order_date,
                    order_time,
                    status,
                    total_amount,
                    payment_status,
                    payment_method
                FROM orders
                ORDER BY order_id DESC
                """
            )

            rows = cursor.fetchall()

            orders = []

            for row in rows:

                order = Order(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9]
                )

                orders.append(order)

            return orders

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - GET BY ID
    # =========================================================

    def get_order_by_id(
        self,
        order_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    order_id,
                    customer_id,
                    user_id,
                    table_id,
                    order_date,
                    order_time,
                    status,
                    total_amount,
                    payment_status,
                    payment_method
                FROM orders
                WHERE order_id = %s
                """,
                (order_id,)
            )

            row = cursor.fetchone()

            if row is None:

                return None

            order = Order(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9]
            )

            return order

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER ITEM - READ ALL
    # =========================================================

    def get_all_order_items(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    order_item_id,
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                FROM order_item
                ORDER BY order_item_id
                """
            )

            rows = cursor.fetchall()

            order_items = []

            for row in rows:

                order_item = OrderItem(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                )

                order_items.append(
                    order_item
                )

            return order_items

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # OPEN ORDER - CREATE
    # =========================================================

    def create_open_order(
        self,
        customer_id,
        user_id,
        table_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Check customer
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT customer_id
                FROM customer
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            if customer is None:

                return (
                    False,
                    "Customer not found."
                )


            # -------------------------------------------------
            # Check user / waiter
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = %s
                """,
                (user_id,)
            )

            user = cursor.fetchone()

            if user is None:

                return (
                    False,
                    "User not found."
                )


            # -------------------------------------------------
            # Check table
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    table_id,
                    status
                FROM cafe_table
                WHERE table_id = %s
                FOR UPDATE
                """,
                (table_id,)
            )

            table = cursor.fetchone()

            if table is None:

                return (
                    False,
                    "Table not found."
                )


            # -------------------------------------------------
            # Check table availability
            # -------------------------------------------------

            if table[1] != "Available":

                return (
                    False,
                    "Selected table is already occupied."
                )


            # -------------------------------------------------
            # Current date and time
            # -------------------------------------------------

            current_datetime = datetime.now()

            order_date = (
                current_datetime.date()
            )

            order_time = (
                current_datetime
                .time()
                .replace(microsecond=0)
            )


            # -------------------------------------------------
            # Create OPEN order
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO orders
                (
                    customer_id,
                    user_id,
                    table_id,
                    order_date,
                    order_time,
                    status,
                    total_amount,
                    payment_status,
                    payment_method
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    customer_id,
                    user_id,
                    table_id,
                    order_date,
                    order_time,
                    "Open",
                    0.00,
                    "Pending",
                    None
                )
            )

            order_id = cursor.lastrowid


            # -------------------------------------------------
            # Mark table as occupied
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE cafe_table
                SET status = 'Occupied'
                WHERE table_id = %s
                """,
                (table_id,)
            )


            # -------------------------------------------------
            # Commit
            # -------------------------------------------------

            connection.commit()

            print(
                "Open order created successfully!"
            )

            print(
                f"Order ID: {order_id}"
            )

            print(
                f"Table ID: {table_id}"
            )

            return (
                True,
                order_id
            )

        except Exception as error:

            connection.rollback()

            print(
                "Could not create open order."
            )

            print(error)

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - ADD ITEM
    # =========================================================

    def add_item_to_order(
        self,
        order_id,
        product_id,
        quantity
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Validate quantity
            # -------------------------------------------------

            if quantity <= 0:

                return (
                    False,
                    "Quantity must be greater than zero."
                )


            # -------------------------------------------------
            # Check order
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_id,
                    status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return (
                    False,
                    "Order not found."
                )


            # -------------------------------------------------
            # Check order status
            # -------------------------------------------------

            if order[1] not in {
                "Open",
                "Preparing",
                "Ready",
                "Served"
            }:

                return (
                    False,
                    "Items cannot be added to this order."
                )


            # -------------------------------------------------
            # Check product
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    product_id,
                    product_name,
                    price,
                    availability
                FROM product
                WHERE product_id = %s
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:

                return (
                    False,
                    "Product not found."
                )


            # -------------------------------------------------
            # Check product availability
            # -------------------------------------------------

            if not product[3]:

                return (
                    False,
                    f"{product[1]} is not available."
                )

            unit_price = product[2]


            # -------------------------------------------------
            # Check whether item already exists
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_item_id,
                    quantity
                FROM order_item
                WHERE order_id = %s
                  AND product_id = %s
                """,
                (
                    order_id,
                    product_id
                )
            )

            existing_item = cursor.fetchone()

            if existing_item is not None:

                new_quantity = (
                    existing_item[1] + quantity
                )

                new_subtotal = (
                    unit_price * new_quantity
                )

                cursor.execute(
                    """
                    UPDATE order_item
                    SET
                        quantity = %s,
                        unit_price = %s,
                        subtotal = %s
                    WHERE order_item_id = %s
                    """,
                    (
                        new_quantity,
                        unit_price,
                        new_subtotal,
                        existing_item[0]
                    )
                )

            else:

                subtotal = (
                    unit_price * quantity
                )

                cursor.execute(
                    """
                    INSERT INTO order_item
                    (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                )


            # -------------------------------------------------
            # Recalculate total
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(subtotal), 0)
                FROM order_item
                WHERE order_id = %s
                """,
                (order_id,)
            )

            total_amount = cursor.fetchone()[0]


            # -------------------------------------------------
            # Update order total
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE orders
                SET total_amount = %s
                WHERE order_id = %s
                """,
                (
                    total_amount,
                    order_id
                )
            )


            # -------------------------------------------------
            # Commit
            # -------------------------------------------------

            connection.commit()

            print(
                "Item added to order successfully!"
            )

            print(
                f"Order ID: {order_id}"
            )

            print(
                f"Product ID: {product_id}"
            )

            print(
                f"Quantity added: {quantity}"
            )

            print(
                f"Updated Total: {total_amount}"
            )

            return (
                True,
                total_amount
            )

        except Exception as error:

            connection.rollback()

            print(
                "Could not add item to order."
            )

            print(error)

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - GET ITEMS
    # =========================================================

    def get_order_items(
        self,
        order_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    oi.order_item_id,
                    oi.order_id,
                    oi.product_id,
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM order_item oi
                JOIN product p
                    ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """,
                (order_id,)
            )

            rows = cursor.fetchall()

            return rows

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # OPEN ORDER - GET OPEN ORDERS
    # =========================================================

    def get_open_orders(self):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    o.order_id,
                    o.customer_id,
                    c.name AS customer_name,
                    o.user_id,
                    o.table_id,
                    t.table_number,
                    o.order_date,
                    o.order_time,
                    o.status,
                    o.total_amount,
                    o.payment_status,
                    o.payment_method
                FROM orders o
                JOIN customer c
                    ON o.customer_id = c.customer_id
                LEFT JOIN cafe_table t
                    ON o.table_id = t.table_id
                WHERE o.status IN (
                    'Open',
                    'Preparing',
                    'Ready',
                    'Served'
                )
                ORDER BY o.order_id DESC
                """
            )

            rows = cursor.fetchall()

            return rows

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER ITEM - UPDATE QUANTITY
    # =========================================================

    def update_order_item_quantity(
        self,
        order_item_id,
        quantity
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Validate quantity
            # -------------------------------------------------

            if quantity <= 0:

                return (
                    False,
                    "Quantity must be greater than zero."
                )


            # -------------------------------------------------
            # Get existing order item
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_item_id,
                    order_id,
                    product_id
                FROM order_item
                WHERE order_item_id = %s
                FOR UPDATE
                """,
                (order_item_id,)
            )

            item = cursor.fetchone()

            if item is None:

                return (
                    False,
                    "Order item not found."
                )

            order_id = item[1]
            product_id = item[2]


            # -------------------------------------------------
            # Check order status
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return (
                    False,
                    "Order not found."
                )

            if order[0] not in {
                "Open",
                "Preparing"
            }:

                return (
                    False,
                    "This order cannot be modified."
                )


            # -------------------------------------------------
            # Get current product price
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT price
                FROM product
                WHERE product_id = %s
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:

                return (
                    False,
                    "Product not found."
                )

            unit_price = product[0]

            subtotal = (
                unit_price * quantity
            )


            # -------------------------------------------------
            # Update order item
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE order_item
                SET
                    quantity = %s,
                    unit_price = %s,
                    subtotal = %s
                WHERE order_item_id = %s
                """,
                (
                    quantity,
                    unit_price,
                    subtotal,
                    order_item_id
                )
            )


            # -------------------------------------------------
            # Recalculate order total
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(subtotal), 0)
                FROM order_item
                WHERE order_id = %s
                """,
                (order_id,)
            )

            total_amount = cursor.fetchone()[0]


            # -------------------------------------------------
            # Update order total
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE orders
                SET total_amount = %s
                WHERE order_id = %s
                """,
                (
                    total_amount,
                    order_id
                )
            )


            # -------------------------------------------------
            # Commit
            # -------------------------------------------------

            connection.commit()

            print(
                "Order item quantity updated successfully!"
            )

            print(
                f"Order Item ID: {order_item_id}"
            )

            print(
                f"New Quantity: {quantity}"
            )

            print(
                f"Updated Total: {total_amount}"
            )

            return (
                True,
                total_amount
            )

        except Exception as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER ITEM - REMOVE
    # =========================================================

    def remove_order_item(
        self,
        order_item_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Get order ID
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_item_id,
                    order_id
                FROM order_item
                WHERE order_item_id = %s
                FOR UPDATE
                """,
                (order_item_id,)
            )

            item = cursor.fetchone()

            if item is None:

                return (
                    False,
                    "Order item not found."
                )

            order_id = item[1]


            # -------------------------------------------------
            # Check order status
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return (
                    False,
                    "Order not found."
                )

            if order[0] not in {
                "Open",
                "Preparing"
            }:

                return (
                    False,
                    "This order cannot be modified."
                )


            # -------------------------------------------------
            # Delete item
            # -------------------------------------------------

            cursor.execute(
                """
                DELETE FROM order_item
                WHERE order_item_id = %s
                """,
                (order_item_id,)
            )


            # -------------------------------------------------
            # Recalculate total
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    COALESCE(SUM(subtotal), 0)
                FROM order_item
                WHERE order_id = %s
                """,
                (order_id,)
            )

            total_amount = cursor.fetchone()[0]


            # -------------------------------------------------
            # Update order total
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE orders
                SET total_amount = %s
                WHERE order_id = %s
                """,
                (
                    total_amount,
                    order_id
                )
            )


            # -------------------------------------------------
            # Commit
            # -------------------------------------------------

            connection.commit()

            print(
                "Order item removed successfully!"
            )

            print(
                f"Order Item ID: {order_item_id}"
            )

            print(
                f"Updated Total: {total_amount}"
            )

            return (
                True,
                total_amount
            )

        except Exception as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - CREATE (OLD FLOW)
    # =========================================================

    def create_order(
        self,
        customer_id,
        user_id,
        items
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            total_amount = 0

            product_details = []


            # -----------------------------------------
            # Check products and calculate total
            # -----------------------------------------

            for product_id, quantity in items:

                query = """
                    SELECT
                        product_id,
                        product_name,
                        price,
                        availability
                    FROM product
                    WHERE product_id = %s
                """

                cursor.execute(
                    query,
                    (product_id,)
                )

                product = cursor.fetchone()

                if product is None:

                    message = (
                        f"Product ID {product_id} not found."
                    )

                    connection.rollback()

                    return (
                        False,
                        message,
                        0
                    )

                if not product[3]:

                    message = (
                        f"{product[1]} is not available."
                    )

                    connection.rollback()

                    return (
                        False,
                        message,
                        0
                    )

                if quantity <= 0:

                    message = (
                        "Quantity must be greater than 0."
                    )

                    connection.rollback()

                    return (
                        False,
                        message,
                        0
                    )

                unit_price = product[2]

                subtotal = (
                    unit_price * quantity
                )

                total_amount += subtotal

                product_details.append(
                    (
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                )


            # -----------------------------------------
            # Create order
            # -----------------------------------------

            current_datetime = datetime.now()

            order_date = current_datetime.date()

            order_time = current_datetime.time()

            order_query = """
                INSERT INTO orders
                (
                    customer_id,
                    user_id,
                    order_date,
                    order_time,
                    status,
                    total_amount
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            order_values = (
                customer_id,
                user_id,
                order_date,
                order_time,
                "Pending",
                total_amount
            )

            cursor.execute(
                order_query,
                order_values
            )

            order_id = cursor.lastrowid


            # -----------------------------------------
            # Create order items
            # -----------------------------------------

            item_query = """
                INSERT INTO order_item
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                )
                VALUES (%s, %s, %s, %s, %s)
            """

            for (
                product_id,
                quantity,
                unit_price,
                subtotal
            ) in product_details:

                item_values = (
                    order_id,
                    product_id,
                    quantity,
                    unit_price,
                    subtotal
                )

                cursor.execute(
                    item_query,
                    item_values
                )


            connection.commit()

            print(
                "Order created successfully!"
            )

            print(
                f"Order ID: {order_id}"
            )

            print(
                f"Total Amount: {total_amount}"
            )

            return (
                True,
                order_id,
                total_amount
            )

        except IntegrityError as error:

            connection.rollback()

            print(
                "Could not create order."
            )

            print(error)

            return (
                False,
                str(error),
                0
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - UPDATE STATUS
    # =========================================================

    def update_order_status(
        self,
        order_id,
        status
    ):

        connection = get_connection()
        cursor = connection.cursor()

        valid_statuses = {
            "Open",
            "Preparing",
            "Ready",
            "Served",
            "Completed",
            "Cancelled"
        }

        if status not in valid_statuses:

            cursor.close()
            connection.close()

            return (
                False,
                "Invalid order status."
            )

        query = """
            UPDATE orders
            SET status = %s
            WHERE order_id = %s
        """

        values = (
            status,
            order_id
        )

        try:

            cursor.execute(
                query,
                values
            )

            connection.commit()

            if cursor.rowcount > 0:

                message = (
                    "Order status updated successfully."
                )

                print(message)

                return (
                    True,
                    message
                )

            message = "Order not found."

            print(message)

            return (
                False,
                message
            )

        except IntegrityError as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - CANCEL
    # =========================================================

    def cancel_order(
        self,
        order_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # GET ORDER DETAILS
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_id,
                    table_id,
                    status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()


            # -------------------------------------------------
            # ORDER NOT FOUND
            # -------------------------------------------------

            if order is None:

                return (
                    False,
                    "Order not found."
                )


            table_id = order[1]

            current_status = order[2]


            # -------------------------------------------------
            # PREVENT INVALID CANCELLATION
            # -------------------------------------------------

            if current_status == "Completed":

                return (
                    False,
                    "Completed order cannot be cancelled."
                )


            if current_status == "Cancelled":

                return (
                    False,
                    "Order is already cancelled."
                )


            # -------------------------------------------------
            # CANCEL ORDER
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE orders
                SET status = 'Cancelled'
                WHERE order_id = %s
                """,
                (order_id,)
            )


            # -------------------------------------------------
            # RELEASE TABLE
            # -------------------------------------------------

            if table_id is not None:

                cursor.execute(
                    """
                    UPDATE cafe_table
                    SET status = 'Available'
                    WHERE table_id = %s
                    """,
                    (table_id,)
                )


            # -------------------------------------------------
            # COMMIT
            # -------------------------------------------------

            connection.commit()


            message = (
                "Order cancelled successfully. "
                "The table is now available."
            )


            print(message)

            print(
                f"Order ID: {order_id}"
            )

            print(
                f"Table ID: {table_id}"
            )


            return (
                True,
                message
            )


        except Exception as error:

            connection.rollback()

            print(
                "Could not cancel order."
            )

            print(error)


            return (
                False,
                str(error)
            )


        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - CHECKOUT
    # =========================================================

    def checkout_order(
        self,
        order_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Get order
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_id,
                    status,
                    total_amount,
                    payment_status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return (
                    False,
                    "Order not found.",
                    0
                )


            # -------------------------------------------------
            # Check status
            # -------------------------------------------------

            if order[1] in {
                "Completed",
                "Cancelled"
            }:

                return (
                    False,
                    "This order cannot be checked out.",
                    0
                )


            # -------------------------------------------------
            # Check items
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM order_item
                WHERE order_id = %s
                """,
                (order_id,)
            )

            item_count = cursor.fetchone()[0]

            if item_count == 0:

                return (
                    False,
                    "Order has no items.",
                    0
                )


            # -------------------------------------------------
            # Get total
            # -------------------------------------------------

            total_amount = order[2]

            if total_amount is None or total_amount <= 0:

                return (
                    False,
                    "Order total must be greater than zero.",
                    0
                )


            return (
                True,
                "Order ready for payment.",
                total_amount
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # PAYMENT - MAKE PAYMENT
    # =========================================================

    def make_payment(
        self,
        order_id,
        payment_method
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Validate payment method
            # -------------------------------------------------

            valid_payment_methods = {
                "Cash",
                "Card",
                "QR"
            }

            if payment_method not in valid_payment_methods:

                return (
                    False,
                    "Invalid payment method."
                )


            # -------------------------------------------------
            # Get order
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    order_id,
                    table_id,
                    status,
                    total_amount,
                    payment_status
                FROM orders
                WHERE order_id = %s
                FOR UPDATE
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return (
                    False,
                    "Order not found."
                )

            table_id = order[1]
            status = order[2]
            total_amount = order[3]
            payment_status = order[4]


            # -------------------------------------------------
            # Check order status
            # -------------------------------------------------

            if status == "Cancelled":

                return (
                    False,
                    "Cancelled order cannot be paid."
                )

            if status == "Completed":

                return (
                    False,
                    "Order is already completed."
                )


            # -------------------------------------------------
            # Check payment status
            # -------------------------------------------------

            if payment_status == "Paid":

                return (
                    False,
                    "Order is already paid."
                )


            # -------------------------------------------------
            # Validate total
            # -------------------------------------------------

            if total_amount is None or total_amount <= 0:

                return (
                    False,
                    "Order total must be greater than zero."
                )


            # -------------------------------------------------
            # Check order items
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM order_item
                WHERE order_id = %s
                """,
                (order_id,)
            )

            item_count = cursor.fetchone()[0]

            if item_count == 0:

                return (
                    False,
                    "Order has no items."
                )


            # -------------------------------------------------
            # Create payment
            # -------------------------------------------------

            current_datetime = datetime.now()

            cursor.execute(
                """
                INSERT INTO payment
                (
                    order_id,
                    amount,
                    payment_method,
                    payment_status,
                    payment_date
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    order_id,
                    total_amount,
                    payment_method,
                    "Paid",
                    current_datetime
                )
            )

            payment_id = cursor.lastrowid


            # -------------------------------------------------
            # Update order
            # -------------------------------------------------

            cursor.execute(
                """
                UPDATE orders
                SET
                    status = 'Completed',
                    payment_status = 'Paid',
                    payment_method = %s
                WHERE order_id = %s
                """,
                (
                    payment_method,
                    order_id
                )
            )


            # -------------------------------------------------
            # Release table
            # -------------------------------------------------

            if table_id is not None:

                cursor.execute(
                    """
                    UPDATE cafe_table
                    SET status = 'Available'
                    WHERE table_id = %s
                    """,
                    (table_id,)
                )


            # -------------------------------------------------
            # Commit transaction
            # -------------------------------------------------

            connection.commit()

            return (
                True,
                {
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "amount": total_amount,
                    "payment_method": payment_method,
                    "payment_status": "Paid"
                }
            )

        except Exception as error:

            connection.rollback()

            return (
                False,
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER - GET SUMMARY
    # =========================================================

    def get_order_summary(
        self,
        order_id
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Get order information
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    o.order_id,
                    c.name AS customer_name,
                    o.user_id,
                    o.table_id,
                    t.table_number,
                    o.order_date,
                    o.order_time,
                    o.status,
                    o.total_amount,
                    o.payment_status,
                    o.payment_method
                FROM orders o
                JOIN customer c
                    ON o.customer_id = c.customer_id
                LEFT JOIN cafe_table t
                    ON o.table_id = t.table_id
                WHERE o.order_id = %s
                """,
                (order_id,)
            )

            order = cursor.fetchone()

            if order is None:

                return None


            # -------------------------------------------------
            # Get items
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    oi.product_id,
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM order_item oi
                JOIN product p
                    ON oi.product_id = p.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """,
                (order_id,)
            )

            items = cursor.fetchall()


            # -------------------------------------------------
            # Return summary
            # -------------------------------------------------

            return {
                "order_id": order[0],
                "customer_name": order[1],
                "user_id": order[2],
                "table_id": order[3],
                "table_number": order[4],
                "order_date": order[5],
                "order_time": order[6],
                "status": order[7],
                "total_amount": order[8],
                "payment_status": order[9],
                "payment_method": order[10],
                "items": items
            }

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # POS CHECKOUT (OLD FLOW)
    # =========================================================

    def create_pos_order(
        self,
        customer_id,
        cart_items,
        payment_method
    ):

        connection = get_connection()
        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # Validate payment method
            # -------------------------------------------------

            valid_payment_methods = {
                "Cash",
                "Card",
                "QR"
            }

            if payment_method not in valid_payment_methods:

                return (
                    False,
                    "Invalid payment method.",
                    0
                )


            # -------------------------------------------------
            # Validate cart
            # -------------------------------------------------

            if not cart_items:

                return (
                    False,
                    "Cart is empty.",
                    0
                )


            # -------------------------------------------------
            # Check customer
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT customer_id
                FROM customer
                WHERE customer_id = %s
                """,
                (customer_id,)
            )

            customer = cursor.fetchone()

            if customer is None:

                return (
                    False,
                    "Customer not found.",
                    0
                )


            # -------------------------------------------------
            # Validate products
            # -------------------------------------------------

            validated_items = []

            total_amount = 0

            for item in cart_items:

                product_id = int(
                    item["product_id"]
                )

                quantity = int(
                    item["quantity"]
                )

                if quantity <= 0:

                    return (
                        False,
                        "Quantity must be greater than zero.",
                        0
                    )

                cursor.execute(
                    """
                    SELECT
                        product_name,
                        price,
                        availability
                    FROM product
                    WHERE product_id = %s
                    """,
                    (product_id,)
                )

                product = cursor.fetchone()

                if product is None:

                    return (
                        False,
                        f"Product ID {product_id} not found.",
                        0
                    )

                product_name = product[0]

                unit_price = product[1]

                availability = product[2]


                # -------------------------------------------------
                # Check availability
                # -------------------------------------------------

                if not availability:

                    return (
                        False,
                        f"{product_name} is not available.",
                        0
                    )


                # -------------------------------------------------
                # Calculate subtotal
                # -------------------------------------------------

                subtotal = (
                    unit_price * quantity
                )

                total_amount += subtotal

                validated_items.append(
                    (
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                )


            # -------------------------------------------------
            # Date and time
            # -------------------------------------------------

            current_datetime = datetime.now()

            order_date = (
                current_datetime.date()
            )

            order_time = (
                current_datetime
                .time()
                .replace(microsecond=0)
            )


            # -------------------------------------------------
            # Create completed order
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO orders
                (
                    customer_id,
                    user_id,
                    order_date,
                    order_time,
                    status,
                    total_amount,
                    payment_status,
                    payment_method
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    customer_id,
                    None,
                    order_date,
                    order_time,
                    "Completed",
                    total_amount,
                    "Paid",
                    payment_method
                )
            )

            order_id = cursor.lastrowid


            # -------------------------------------------------
            # Create order items
            # -------------------------------------------------

            for item in validated_items:

                product_id = item[0]

                quantity = item[1]

                unit_price = item[2]

                subtotal = item[3]

                cursor.execute(
                    """
                    INSERT INTO order_item
                    (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        order_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                )


            # -------------------------------------------------
            # Commit transaction
            # -------------------------------------------------

            connection.commit()

            return (
                True,
                order_id,
                total_amount
            )

        except Exception as error:

            connection.rollback()

            return (
                False,
                str(error),
                0
            )

        finally:

            cursor.close()
            connection.close()


    # =========================================================
    # ORDER HISTORY
    # =========================================================

    def get_order_history(self):

        connection = get_connection()

        cursor = connection.cursor(
            buffered=True
        )

        query = """
            SELECT
                o.order_id,
                o.order_date,
                o.order_time,
                c.name AS customer_name,
                o.status,
                o.total_amount,
                o.payment_method
            FROM orders o
            JOIN customer c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC
        """

        try:

            cursor.execute(
                query
            )

            rows = cursor.fetchall()

            return rows

        finally:

            cursor.close()
            connection.close()