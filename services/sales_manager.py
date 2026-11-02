"""Business logic and database operations for the My Cafe POS application.

This module preserves the public SalesManager methods used by the existing
Streamlit pages and command-line interface while centralising validation,
connection cleanup, transaction handling, and order/payment rules.
"""

from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import hashlib
import hmac
import secrets

from mysql.connector import IntegrityError

from database.connection import get_connection
from models.product import Product
from models.customer import Customer
from models.user import User
from models.order import Order
from models.order_item import OrderItem
from models.cafe_table import CafeTable


class SalesManager:
    """Coordinate product, customer, table, user, order and payment data."""

    ACTIVE_ORDER_STATUSES = ("Open", "Preparing", "Ready", "Served")
    EDITABLE_ORDER_STATUSES = ("Open", "Preparing")
    VALID_TABLE_STATUSES = ("Available", "Occupied")
    VALID_PAYMENT_METHODS = ("Cash", "Card", "QR")
    VALID_USER_ROLES = ("Admin", "Staff", "Owner")

    PASSWORD_HASH_NAME = "pbkdf2_sha256"
    PASSWORD_HASH_ITERATIONS = 260_000
    MONEY_QUANTUM = Decimal("0.01")

    # =========================================================
    # SHARED HELPERS
    # =========================================================

    @contextmanager
    def _db_cursor(self, buffered=False):
        """Open a connection/cursor and always close both safely.

        Any uncaught exception causes a rollback before the connection closes.
        Individual write methods commit only after all related writes succeed.
        """
        connection = get_connection()
        cursor = None
        try:
            if buffered:
                cursor = connection.cursor(buffered=True)
            else:
                cursor = connection.cursor()
            yield connection, cursor
        except Exception:
            try:
                connection.rollback()
            except Exception:
                pass
            raise
        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass
            try:
                connection.close()
            except Exception:
                pass

    @staticmethod
    def _failure(connection, message, *extra_values):
        """Roll back a transaction and return a standard failure tuple."""
        try:
            connection.rollback()
        except Exception:
            pass
        return (False, message, *extra_values)

    @staticmethod
    def _required_text(value, field_name, max_length=None):
        if value is None:
            raise ValueError(f"{field_name} is required.")
        cleaned = str(value).strip()
        if not cleaned:
            raise ValueError(f"{field_name} is required.")
        if max_length is not None and len(cleaned) > max_length:
            raise ValueError(
                f"{field_name} must be {max_length} characters or fewer."
            )
        return cleaned

    @classmethod
    def _positive_id(cls, value, field_name="ID"):
        try:
            number = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must be a positive integer.")
        if isinstance(value, bool) or number <= 0:
            raise ValueError(f"{field_name} must be a positive integer.")
        try:
            if Decimal(str(value)) != Decimal(number):
                raise ValueError(f"{field_name} must be a whole number.")
        except InvalidOperation:
            raise ValueError(f"{field_name} must be a positive integer.")
        return number

    @classmethod
    def _quantity(cls, value, maximum=50):
        quantity = cls._positive_id(value, "Quantity")
        if quantity > maximum:
            raise ValueError(f"Quantity cannot exceed {maximum}.")
        return quantity

    @classmethod
    def _money(cls, value, field_name="Price", allow_zero=False):
        try:
            amount = Decimal(str(value))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError(f"{field_name} must be a valid number.")
        if not amount.is_finite():
            raise ValueError(f"{field_name} must be a finite number.")
        if amount < 0 or (amount == 0 and not allow_zero):
            comparison = "zero or greater" if allow_zero else "greater than zero"
            raise ValueError(f"{field_name} must be {comparison}.")
        try:
            return amount.quantize(cls.MONEY_QUANTUM, rounding=ROUND_HALF_UP)
        except InvalidOperation:
            raise ValueError(f"{field_name} is outside the supported range.")

    @classmethod
    def _phone_number(cls, value):
        phone = cls._required_text(value, "Phone number", max_length=15)
        if not phone.isdigit() or not 9 <= len(phone) <= 15:
            raise ValueError(
                "Phone number must contain 9 to 15 digits only."
            )
        return phone

    @classmethod
    def _hash_password(cls, password):
        password = cls._required_text(password, "Password")
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            cls.PASSWORD_HASH_ITERATIONS,
        )
        return "{}${}${}${}".format(
            cls.PASSWORD_HASH_NAME,
            cls.PASSWORD_HASH_ITERATIONS,
            salt.hex(),
            digest.hex(),
        )

    @classmethod
    def _verify_password_hash(cls, password, stored_value):
        """Verify a PBKDF2 hash. Return False for malformed stored values."""
        try:
            algorithm, iterations_text, salt_hex, digest_hex = str(
                stored_value
            ).split("$", 3)
            if algorithm != cls.PASSWORD_HASH_NAME:
                return False
            iterations = int(iterations_text)
            if iterations < 100_000 or iterations > 2_000_000:
                return False
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(digest_hex)
            actual = hashlib.pbkdf2_hmac(
                "sha256",
                str(password).encode("utf-8"),
                salt,
                iterations,
            )
            return hmac.compare_digest(actual, expected)
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _recalculate_order_total(cursor, order_id):
        cursor.execute(
            """
            SELECT COALESCE(SUM(subtotal), 0)
            FROM order_item
            WHERE order_id = %s
            """,
            (order_id,),
        )
        return Decimal(str(cursor.fetchone()[0] or 0)).quantize(
            Decimal("0.01")
        )

    @classmethod
    def _release_table_if_unused(cls, cursor, table_id, current_order_id):
        """Free a table only when no other active order still uses it."""
        if table_id is None:
            return
        placeholders = ", ".join(["%s"] * len(cls.ACTIVE_ORDER_STATUSES))
        query = f"""
            UPDATE cafe_table AS ct
            SET ct.status = 'Available'
            WHERE ct.table_id = %s
              AND NOT EXISTS (
                    SELECT 1
                    FROM orders AS other_order
                    WHERE other_order.table_id = ct.table_id
                      AND other_order.order_id <> %s
                      AND other_order.status IN ({placeholders})
              )
        """
        cursor.execute(
            query,
            (table_id, current_order_id, *cls.ACTIVE_ORDER_STATUSES),
        )

    @staticmethod
    def _find_record(cursor, table_name, id_column, record_id):
        cursor.execute(
            f"SELECT {id_column} FROM {table_name} WHERE {id_column} = %s",
            (record_id,),
        )
        return cursor.fetchone() is not None

    # =========================================================
    # PRODUCT - READ / CREATE / UPDATE / DELETE
    # =========================================================

    def get_all_products(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT product_id, product_name, category, price,
                       availability, image_url
                FROM product
                ORDER BY product_id
                """
            )
            return [Product(*row) for row in cursor.fetchall()]

    def add_product(
        self,
        product_name,
        category,
        price,
        availability=True,
        image_url=None,
    ):
        try:
            product_name = self._required_text(
                product_name, "Product name", 150
            )
            category = self._required_text(category, "Category", 100)
            price = self._money(price)
            if image_url is not None:
                image_url = str(image_url).strip() or None
        except ValueError as error:
            return False, str(error)

        try:
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    INSERT INTO product
                        (product_name, category, price, availability, image_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (product_name, category, price, bool(availability), image_url),
                )
                product_id = cursor.lastrowid
                connection.commit()
                return True, product_id
        except IntegrityError as error:
            return False, str(error)
        except Exception as error:
            return False, str(error)

    def update_product(
        self,
        product_id,
        product_name,
        category,
        price,
        availability,
        image_url=None,
    ):
        try:
            product_id = self._positive_id(product_id, "Product ID")
            product_name = self._required_text(
                product_name, "Product name", 150
            )
            category = self._required_text(category, "Category", 100)
            price = self._money(price)
            if image_url is not None:
                image_url = str(image_url).strip() or None
        except ValueError as error:
            return False, str(error)

        try:
            with self._db_cursor() as (connection, cursor):
                # None means "leave the existing image unchanged". This is
                # important because the current Product Management form does
                # not submit an image_url when editing other product fields.
                cursor.execute(
                    """
                    UPDATE product
                    SET product_name = %s,
                        category = %s,
                        price = %s,
                        availability = %s,
                        image_url = COALESCE(%s, image_url)
                    WHERE product_id = %s
                    """,
                    (
                        product_name,
                        category,
                        price,
                        bool(availability),
                        image_url,
                        product_id,
                    ),
                )
                changed_rows = cursor.rowcount
                if changed_rows == 0:
                    exists = self._find_record(
                        cursor, "product", "product_id", product_id
                    )
                    connection.commit()
                    if not exists:
                        return False, "Product not found."
                    return True, "No changes were necessary."
                connection.commit()
                return True, "Product updated successfully."
        except IntegrityError as error:
            return False, str(error)
        except Exception as error:
            return False, str(error)

    def delete_product(self, product_id):
        try:
            product_id = self._positive_id(product_id, "Product ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "DELETE FROM product WHERE product_id = %s",
                    (product_id,),
                )
                if cursor.rowcount == 0:
                    connection.commit()
                    return False, "Product not found."
                connection.commit()
                return True, "Product deleted successfully."
        except IntegrityError:
            return (
                False,
                "Cannot delete this product because it is used in existing orders. "
                "Mark it unavailable instead to preserve order history.",
            )
        except Exception as error:
            return False, str(error)

    # =========================================================
    # CUSTOMER - READ / CREATE / UPDATE / DELETE
    # =========================================================

    def get_all_customers(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT customer_id, name, phone
                FROM customer
                ORDER BY customer_id
                """
            )
            return [Customer(*row) for row in cursor.fetchall()]

    def add_customer(self, name, phone):
        try:
            name = self._required_text(name, "Customer name", 150)
            phone = self._phone_number(phone)
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "SELECT customer_id, name FROM customer WHERE phone = %s",
                    (phone,),
                )
                duplicate = cursor.fetchone()
                if duplicate:
                    return self._failure(
                        connection,
                        f"Phone number is already registered to {duplicate[1]}.",
                    )
                cursor.execute(
                    "INSERT INTO customer (name, phone) VALUES (%s, %s)",
                    (name, phone),
                )
                customer_id = cursor.lastrowid
                connection.commit()
                return True, customer_id
        except IntegrityError as error:
            return False, str(error)
        except Exception as error:
            return False, str(error)

    def update_customer(self, customer_id, name, phone):
        try:
            customer_id = self._positive_id(customer_id, "Customer ID")
            name = self._required_text(name, "Customer name", 150)
            phone = self._phone_number(phone)
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT customer_id, name
                    FROM customer
                    WHERE phone = %s AND customer_id <> %s
                    """,
                    (phone, customer_id),
                )
                duplicate = cursor.fetchone()
                if duplicate:
                    return self._failure(
                        connection,
                        f"Phone number is already registered to {duplicate[1]}.",
                    )
                cursor.execute(
                    """
                    UPDATE customer
                    SET name = %s, phone = %s
                    WHERE customer_id = %s
                    """,
                    (name, phone, customer_id),
                )
                if cursor.rowcount == 0:
                    exists = self._find_record(
                        cursor, "customer", "customer_id", customer_id
                    )
                    connection.commit()
                    if not exists:
                        return False, "Customer not found."
                    return True, "No changes were necessary."
                connection.commit()
                return True, "Customer updated successfully."
        except IntegrityError as error:
            return False, str(error)
        except Exception as error:
            return False, str(error)

    def delete_customer(self, customer_id):
        try:
            customer_id = self._positive_id(customer_id, "Customer ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "DELETE FROM customer WHERE customer_id = %s",
                    (customer_id,),
                )
                if cursor.rowcount == 0:
                    connection.commit()
                    return False, "Customer not found."
                connection.commit()
                return True, "Customer deleted successfully."
        except IntegrityError:
            return (
                False,
                "Cannot delete this customer because existing orders are linked "
                "to this customer. Keep the record to preserve order history.",
            )
        except Exception as error:
            return False, str(error)

    # =========================================================
    # TABLE - READ / UPDATE STATUS
    # =========================================================

    def get_all_tables(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT table_id, table_number, capacity, status
                FROM cafe_table
                ORDER BY table_id
                """
            )
            return [CafeTable(*row) for row in cursor.fetchall()]

    def get_available_tables(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT table_id, table_number, capacity, status
                FROM cafe_table
                WHERE status = 'Available'
                ORDER BY table_id
                """
            )
            return [CafeTable(*row) for row in cursor.fetchall()]

    def update_table_status(self, table_id, status):
        try:
            table_id = self._positive_id(table_id, "Table ID")
            status = self._required_text(status, "Table status")
            if status not in self.VALID_TABLE_STATUSES:
                return False, "Table status must be Available or Occupied."
            with self._db_cursor() as (connection, cursor):
                if status == "Available":
                    placeholders = ", ".join(
                        ["%s"] * len(self.ACTIVE_ORDER_STATUSES)
                    )
                    cursor.execute(
                        f"""
                        SELECT order_id
                        FROM orders
                        WHERE table_id = %s
                          AND status IN ({placeholders})
                        LIMIT 1
                        FOR UPDATE
                        """,
                        (table_id, *self.ACTIVE_ORDER_STATUSES),
                    )
                    if cursor.fetchone():
                        return self._failure(
                            connection,
                            "This table has an active order and cannot be marked available.",
                        )
                cursor.execute(
                    "UPDATE cafe_table SET status = %s WHERE table_id = %s",
                    (status, table_id),
                )
                if cursor.rowcount == 0:
                    exists = self._find_record(
                        cursor, "cafe_table", "table_id", table_id
                    )
                    connection.commit()
                    if not exists:
                        return False, "Table not found."
                    return True, "No changes were necessary."
                connection.commit()
                return True, "Table status updated successfully."
        except Exception as error:
            return False, str(error)

    # =========================================================
    # USER - READ / CREATE / UPDATE / DELETE / AUTHENTICATION
    # =========================================================

    def get_all_users(self):
        """Return user profiles without retrieving password hashes."""
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT user_id, name, username, role
                FROM users
                ORDER BY user_id
                """
            )
            return [
                User(row[0], row[1], row[2], None, row[3])
                for row in cursor.fetchall()
            ]

    def add_user(self, name, username, password, role):
        try:
            name = self._required_text(name, "Name", 150)
            username = self._required_text(username, "Username", 100)
            role = self._required_text(role, "Role", 30)
            if role not in self.VALID_USER_ROLES:
                return False, "Role must be Admin, Staff or Owner."
            password_hash = self._hash_password(password)
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    INSERT INTO users (name, username, password, role)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (name, username, password_hash, role),
                )
                user_id = cursor.lastrowid
                connection.commit()
                return True, user_id
        except IntegrityError:
            return False, "Username already exists. Please choose another username."
        except Exception as error:
            return False, str(error)

    def update_user(self, user_id, name, username, password=None, role=None):
        try:
            user_id = self._positive_id(user_id, "User ID")
            name = self._required_text(name, "Name", 150)
            username = self._required_text(username, "Username", 100)
            role = self._required_text(role, "Role", 30)
            if role not in self.VALID_USER_ROLES:
                return False, "Role must be Admin, Staff or Owner."
            with self._db_cursor() as (connection, cursor):
                if password is not None and str(password).strip():
                    password_hash = self._hash_password(password)
                    cursor.execute(
                        """
                        UPDATE users
                        SET name = %s, username = %s, password = %s, role = %s
                        WHERE user_id = %s
                        """,
                        (name, username, password_hash, role, user_id),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE users
                        SET name = %s, username = %s, role = %s
                        WHERE user_id = %s
                        """,
                        (name, username, role, user_id),
                    )
                if cursor.rowcount == 0:
                    exists = self._find_record(
                        cursor, "users", "user_id", user_id
                    )
                    connection.commit()
                    if not exists:
                        return False, "User not found."
                    return True, "No changes were necessary."
                connection.commit()
                return True, "User updated successfully."
        except IntegrityError:
            return False, "Username already exists. Please choose another username."
        except Exception as error:
            return False, str(error)

    def delete_user(self, user_id):
        try:
            user_id = self._positive_id(user_id, "User ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "DELETE FROM users WHERE user_id = %s",
                    (user_id,),
                )
                if cursor.rowcount == 0:
                    connection.commit()
                    return False, "User not found."
                connection.commit()
                return True, "User deleted successfully."
        except IntegrityError:
            return (
                False,
                "Cannot delete this user because existing orders are linked to this user.",
            )
        except Exception as error:
            return False, str(error)

    def verify_user_credentials(self, username, password):
        """Verify credentials and upgrade a legacy plaintext password on success.

        New passwords are stored as PBKDF2-SHA256 hashes. Existing plaintext
        passwords are accepted once for compatibility and immediately upgraded.
        """
        try:
            username = self._required_text(username, "Username", 100)
            if password is None or str(password) == "":
                return False, "Username or password is incorrect."
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT user_id, name, username, password, role
                    FROM users
                    WHERE username = %s
                    """,
                    (username,),
                )
                row = cursor.fetchone()
                if row is None:
                    return self._failure(
                        connection, "Username or password is incorrect."
                    )

                stored_password = row[3]
                stored_text = str(stored_password or "")
                if stored_text.startswith(self.PASSWORD_HASH_NAME + "$"):
                    valid = self._verify_password_hash(password, stored_text)
                else:
                    valid = hmac.compare_digest(
                        stored_text.encode("utf-8"),
                        str(password).encode("utf-8"),
                    )
                    if valid:
                        # Migrate a legacy plaintext value to a salted hash.
                        cursor.execute(
                            "UPDATE users SET password = %s WHERE user_id = %s",
                            (self._hash_password(password), row[0]),
                        )
                        connection.commit()
                if not valid:
                    return self._failure(
                        connection, "Username or password is incorrect."
                    )
                user = User(row[0], row[1], row[2], None, row[4])
                return True, user
        except Exception as error:
            return False, str(error)

    # =========================================================
    # ORDER - READ
    # =========================================================

    def get_all_orders(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT order_id, customer_id, user_id, table_id,
                       order_date, order_time, status, total_amount,
                       payment_status, payment_method
                FROM orders
                ORDER BY order_id DESC
                """
            )
            return [Order(*row) for row in cursor.fetchall()]

    def get_order_by_id(self, order_id):
        try:
            order_id = self._positive_id(order_id, "Order ID")
            with self._db_cursor() as (_, cursor):
                cursor.execute(
                    """
                    SELECT order_id, customer_id, user_id, table_id,
                           order_date, order_time, status, total_amount,
                           payment_status, payment_method
                    FROM orders
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )
                row = cursor.fetchone()
                return Order(*row) if row else None
        except Exception:
            raise

    def get_all_order_items(self):
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT order_item_id, order_id, product_id,
                       quantity, unit_price, subtotal
                FROM order_item
                ORDER BY order_item_id
                """
            )
            return [OrderItem(*row) for row in cursor.fetchall()]

    # =========================================================
    # OPEN ORDER - CREATE
    # =========================================================

    def create_open_order(self, customer_id, user_id, table_id):
        try:
            customer_id = self._positive_id(customer_id, "Customer ID")
            user_id = self._positive_id(user_id, "User ID")
            table_id = self._positive_id(table_id, "Table ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "SELECT customer_id FROM customer WHERE customer_id = %s",
                    (customer_id,),
                )
                if cursor.fetchone() is None:
                    return self._failure(connection, "Customer not found.")

                cursor.execute(
                    "SELECT user_id FROM users WHERE user_id = %s",
                    (user_id,),
                )
                if cursor.fetchone() is None:
                    return self._failure(connection, "Staff user not found.")

                # Lock the table row so two concurrent requests cannot reserve
                # the same table when the table engine supports transactions.
                cursor.execute(
                    """
                    SELECT table_id, status
                    FROM cafe_table
                    WHERE table_id = %s
                    FOR UPDATE
                    """,
                    (table_id,),
                )
                table = cursor.fetchone()
                if table is None:
                    return self._failure(connection, "Table not found.")
                if table[1] != "Available":
                    return self._failure(
                        connection, "Selected table is not available."
                    )

                placeholders = ", ".join(
                    ["%s"] * len(self.ACTIVE_ORDER_STATUSES)
                )
                cursor.execute(
                    f"""
                    SELECT order_id
                    FROM orders
                    WHERE table_id = %s
                      AND status IN ({placeholders})
                    LIMIT 1
                    FOR UPDATE
                    """,
                    (table_id, *self.ACTIVE_ORDER_STATUSES),
                )
                if cursor.fetchone():
                    return self._failure(
                        connection,
                        "An active order is already linked to this table.",
                    )

                current_datetime = datetime.now()
                cursor.execute(
                    """
                    INSERT INTO orders
                        (customer_id, user_id, table_id, order_date, order_time,
                         status, total_amount, payment_status, payment_method)
                    VALUES (%s, %s, %s, %s, %s, 'Open', %s, 'Pending', NULL)
                    """,
                    (
                        customer_id,
                        user_id,
                        table_id,
                        current_datetime.date(),
                        current_datetime.time().replace(microsecond=0),
                        Decimal("0.00"),
                    ),
                )
                order_id = cursor.lastrowid
                cursor.execute(
                    "UPDATE cafe_table SET status = 'Occupied' WHERE table_id = %s",
                    (table_id,),
                )
                if cursor.rowcount != 1:
                    return self._failure(
                        connection, "Could not reserve the selected table."
                    )
                connection.commit()
                return True, order_id
        except Exception as error:
            return False, str(error)

    # =========================================================
    # ORDER - ADD ITEM / GET ITEMS
    # =========================================================

    def add_item_to_order(self, order_id, product_id, quantity):
        try:
            order_id = self._positive_id(order_id, "Order ID")
            product_id = self._positive_id(product_id, "Product ID")
            quantity = self._quantity(quantity)
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "SELECT status FROM orders WHERE order_id = %s FOR UPDATE",
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                if order[0] not in self.EDITABLE_ORDER_STATUSES:
                    return self._failure(
                        connection,
                        "Products can only be added while an order is Open or Preparing.",
                    )

                cursor.execute(
                    """
                    SELECT product_name, price, availability
                    FROM product
                    WHERE product_id = %s
                    """,
                    (product_id,),
                )
                product = cursor.fetchone()
                if product is None:
                    return self._failure(connection, "Product not found.")
                if not bool(product[2]):
                    return self._failure(
                        connection, f"{product[0]} is not available."
                    )

                cursor.execute(
                    """
                    SELECT order_item_id, quantity, unit_price
                    FROM order_item
                    WHERE order_id = %s AND product_id = %s
                    FOR UPDATE
                    """,
                    (order_id, product_id),
                )
                existing_item = cursor.fetchone()
                if existing_item:
                    new_quantity = int(existing_item[1]) + quantity
                    if new_quantity > 50:
                        return self._failure(
                            connection, "An order item quantity cannot exceed 50."
                        )
                    # Preserve the price captured when the item was first added.
                    unit_price = Decimal(str(existing_item[2]))
                    subtotal = (unit_price * new_quantity).quantize(
                        self.MONEY_QUANTUM
                    )
                    cursor.execute(
                        """
                        UPDATE order_item
                        SET quantity = %s, subtotal = %s
                        WHERE order_item_id = %s
                        """,
                        (new_quantity, subtotal, existing_item[0]),
                    )
                else:
                    unit_price = self._money(product[1])
                    subtotal = (unit_price * quantity).quantize(
                        self.MONEY_QUANTUM
                    )
                    cursor.execute(
                        """
                        INSERT INTO order_item
                            (order_id, product_id, quantity, unit_price, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (order_id, product_id, quantity, unit_price, subtotal),
                    )

                total_amount = self._recalculate_order_total(cursor, order_id)
                cursor.execute(
                    "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                    (total_amount, order_id),
                )
                connection.commit()
                return True, total_amount
        except Exception as error:
            return False, str(error)

    def get_order_items(self, order_id):
        order_id = self._positive_id(order_id, "Order ID")
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                """
                SELECT oi.order_item_id, oi.order_id, oi.product_id,
                       p.product_name, oi.quantity, oi.unit_price, oi.subtotal
                FROM order_item AS oi
                JOIN product AS p ON p.product_id = oi.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """,
                (order_id,),
            )
            return cursor.fetchall()

    def get_open_orders(self):
        placeholders = ", ".join(
            ["%s"] * len(self.ACTIVE_ORDER_STATUSES)
        )
        with self._db_cursor() as (_, cursor):
            cursor.execute(
                f"""
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
                FROM orders AS o
                JOIN customer AS c ON c.customer_id = o.customer_id
                LEFT JOIN cafe_table AS t ON t.table_id = o.table_id
                WHERE o.status IN ({placeholders})
                ORDER BY o.order_id DESC
                """,
                self.ACTIVE_ORDER_STATUSES,
            )
            return cursor.fetchall()

    # =========================================================
    # ORDER ITEM - UPDATE QUANTITY / REMOVE
    # =========================================================

    def update_order_item_quantity(self, order_item_id, quantity):
        try:
            order_item_id = self._positive_id(
                order_item_id, "Order item ID"
            )
            quantity = self._quantity(quantity)
            with self._db_cursor() as (connection, cursor):
                # Read the parent ID first, then lock the order row before
                # locking the item row. All order-item writes use this order
                # to reduce the risk of concurrent transaction deadlocks.
                cursor.execute(
                    "SELECT order_id FROM order_item WHERE order_item_id = %s",
                    (order_item_id,),
                )
                item_reference = cursor.fetchone()
                if item_reference is None:
                    return self._failure(connection, "Order item not found.")
                order_id = item_reference[0]

                cursor.execute(
                    "SELECT status FROM orders WHERE order_id = %s FOR UPDATE",
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                if order[0] not in self.EDITABLE_ORDER_STATUSES:
                    return self._failure(
                        connection, "This order can no longer be modified."
                    )

                cursor.execute(
                    """
                    SELECT unit_price
                    FROM order_item
                    WHERE order_item_id = %s AND order_id = %s
                    FOR UPDATE
                    """,
                    (order_item_id, order_id),
                )
                item = cursor.fetchone()
                if item is None:
                    return self._failure(connection, "Order item no longer exists.")
                unit_price = Decimal(str(item[0]))

                # Keep the unit price snapshot from when the item was added.
                subtotal = (unit_price * quantity).quantize(
                    self.MONEY_QUANTUM
                )
                cursor.execute(
                    """
                    UPDATE order_item
                    SET quantity = %s, subtotal = %s
                    WHERE order_item_id = %s
                    """,
                    (quantity, subtotal, order_item_id),
                )
                total_amount = self._recalculate_order_total(cursor, order_id)
                cursor.execute(
                    "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                    (total_amount, order_id),
                )
                connection.commit()
                return True, total_amount
        except Exception as error:
            return False, str(error)

    def remove_order_item(self, order_item_id):
        try:
            order_item_id = self._positive_id(
                order_item_id, "Order item ID"
            )
            with self._db_cursor() as (connection, cursor):
                # Lock in the same order as quantity updates: order first,
                # then order_item.
                cursor.execute(
                    "SELECT order_id FROM order_item WHERE order_item_id = %s",
                    (order_item_id,),
                )
                item_reference = cursor.fetchone()
                if item_reference is None:
                    return self._failure(connection, "Order item not found.")
                order_id = item_reference[0]

                cursor.execute(
                    "SELECT status FROM orders WHERE order_id = %s FOR UPDATE",
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                if order[0] not in self.EDITABLE_ORDER_STATUSES:
                    return self._failure(
                        connection, "This order can no longer be modified."
                    )

                cursor.execute(
                    """
                    SELECT order_item_id
                    FROM order_item
                    WHERE order_item_id = %s AND order_id = %s
                    FOR UPDATE
                    """,
                    (order_item_id, order_id),
                )
                if cursor.fetchone() is None:
                    return self._failure(connection, "Order item no longer exists.")

                cursor.execute(
                    "DELETE FROM order_item WHERE order_item_id = %s",
                    (order_item_id,),
                )
                total_amount = self._recalculate_order_total(cursor, order_id)
                cursor.execute(
                    "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                    (total_amount, order_id),
                )
                connection.commit()
                return True, total_amount
        except Exception as error:
            return False, str(error)

    # =========================================================
    # LEGACY ORDER CREATION - KEPT FOR THE EXISTING CLI
    # =========================================================

    def create_order(self, customer_id, user_id, items):
        """Create an unpaid Open order for the legacy command-line workflow."""
        try:
            customer_id = self._positive_id(customer_id, "Customer ID")
            user_id = self._positive_id(user_id, "User ID")
            if not items:
                return False, "Order must contain at least one item.", Decimal("0.00")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "SELECT customer_id FROM customer WHERE customer_id = %s",
                    (customer_id,),
                )
                if cursor.fetchone() is None:
                    return self._failure(
                        connection, "Customer not found.", Decimal("0.00")
                    )
                cursor.execute(
                    "SELECT user_id FROM users WHERE user_id = %s",
                    (user_id,),
                )
                if cursor.fetchone() is None:
                    return self._failure(
                        connection, "User not found.", Decimal("0.00")
                    )

                validated_items = []
                total_amount = Decimal("0.00")
                for product_id, quantity in items:
                    product_id = self._positive_id(product_id, "Product ID")
                    quantity = self._quantity(quantity)
                    cursor.execute(
                        """
                        SELECT product_name, price, availability
                        FROM product
                        WHERE product_id = %s
                        """,
                        (product_id,),
                    )
                    product = cursor.fetchone()
                    if product is None:
                        return self._failure(
                            connection,
                            f"Product ID {product_id} not found.",
                            Decimal("0.00"),
                        )
                    if not bool(product[2]):
                        return self._failure(
                            connection,
                            f"{product[0]} is not available.",
                            Decimal("0.00"),
                        )
                    unit_price = self._money(product[1])
                    subtotal = (unit_price * quantity).quantize(
                        self.MONEY_QUANTUM
                    )
                    total_amount += subtotal
                    validated_items.append(
                        (product_id, quantity, unit_price, subtotal)
                    )

                now = datetime.now()
                cursor.execute(
                    """
                    INSERT INTO orders
                        (customer_id, user_id, order_date, order_time,
                         status, total_amount, payment_status, payment_method)
                    VALUES (%s, %s, %s, %s, 'Open', %s, 'Pending', NULL)
                    """,
                    (
                        customer_id,
                        user_id,
                        now.date(),
                        now.time().replace(microsecond=0),
                        total_amount,
                    ),
                )
                order_id = cursor.lastrowid
                for product_id, quantity, unit_price, subtotal in validated_items:
                    cursor.execute(
                        """
                        INSERT INTO order_item
                            (order_id, product_id, quantity, unit_price, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (order_id, product_id, quantity, unit_price, subtotal),
                    )
                connection.commit()
                return True, order_id, total_amount
        except Exception as error:
            return False, str(error), Decimal("0.00")

    # =========================================================
    # ORDER - UPDATE STATUS
    # =========================================================

    def update_order_status(self, order_id, status):
        """Enforce Open -> Preparing -> Ready -> Served only.

        Completed is set only by make_payment(); Cancelled is set only by
        cancel_order().
        """
        try:
            order_id = self._positive_id(order_id, "Order ID")
            status = self._required_text(status, "Order status")
            transitions = {
                "Open": "Preparing",
                "Preparing": "Ready",
                "Ready": "Served",
            }
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT status, payment_status
                    FROM orders
                    WHERE order_id = %s
                    FOR UPDATE
                    """,
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                current_status, payment_status = order
                expected_status = transitions.get(current_status)
                if expected_status is None:
                    return self._failure(
                        connection,
                        f"Order cannot be updated from {current_status}.",
                    )
                if status != expected_status:
                    return self._failure(
                        connection,
                        f"Invalid status transition. Next status must be {expected_status}.",
                    )
                if payment_status == "Paid":
                    return self._failure(
                        connection, "A paid order cannot change its service status."
                    )
                cursor.execute(
                    "UPDATE orders SET status = %s WHERE order_id = %s",
                    (status, order_id),
                )
                connection.commit()
                return True, f"Order status updated to {status}."
        except Exception as error:
            return False, str(error)

    # =========================================================
    # ORDER - CANCEL
    # =========================================================

    def cancel_order(self, order_id):
        try:
            order_id = self._positive_id(order_id, "Order ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT order_id, table_id, status, payment_status
                    FROM orders
                    WHERE order_id = %s
                    FOR UPDATE
                    """,
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                _, table_id, current_status, payment_status = order
                if current_status == "Completed" or payment_status == "Paid":
                    return self._failure(
                        connection, "A paid/completed order cannot be cancelled."
                    )
                if current_status == "Cancelled":
                    return self._failure(connection, "Order is already cancelled.")
                if current_status not in self.ACTIVE_ORDER_STATUSES:
                    return self._failure(
                        connection,
                        f"Order cannot be cancelled from {current_status}.",
                    )

                cursor.execute(
                    "UPDATE orders SET status = 'Cancelled' WHERE order_id = %s",
                    (order_id,),
                )
                self._release_table_if_unused(cursor, table_id, order_id)
                connection.commit()
                return True, "Order cancelled successfully. The table is available if no other active order uses it."
        except Exception as error:
            return False, str(error)

    # =========================================================
    # ORDER - CHECKOUT
    # =========================================================

    def checkout_order(self, order_id):
        try:
            order_id = self._positive_id(order_id, "Order ID")
            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT status, payment_status
                    FROM orders
                    WHERE order_id = %s
                    FOR UPDATE
                    """,
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(
                        connection, "Order not found.", Decimal("0.00")
                    )
                status, payment_status = order
                if status == "Cancelled":
                    return self._failure(
                        connection, "Cancelled orders cannot be checked out.", Decimal("0.00")
                    )
                if status == "Completed" or payment_status == "Paid":
                    return self._failure(
                        connection, "Order is already completed or paid.", Decimal("0.00")
                    )
                if status != "Served":
                    return self._failure(
                        connection,
                        "Order must be marked Served before checkout.",
                        Decimal("0.00"),
                    )

                cursor.execute(
                    "SELECT COUNT(*) FROM payment WHERE order_id = %s",
                    (order_id,),
                )
                if cursor.fetchone()[0] > 0:
                    return self._failure(
                        connection,
                        "A payment record already exists for this order.",
                        Decimal("0.00"),
                    )

                cursor.execute(
                    """
                    SELECT COUNT(*), COALESCE(SUM(subtotal), 0)
                    FROM order_item
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )
                item_count, total_amount = cursor.fetchone()
                total_amount = Decimal(str(total_amount or 0)).quantize(
                    self.MONEY_QUANTUM
                )
                if item_count == 0:
                    return self._failure(
                        connection, "Order has no items.", Decimal("0.00")
                    )
                if total_amount <= 0:
                    return self._failure(
                        connection,
                        "Order total must be greater than zero.",
                        Decimal("0.00"),
                    )
                cursor.execute(
                    "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                    (total_amount, order_id),
                )
                connection.commit()
                return True, "Order ready for payment.", total_amount
        except Exception as error:
            return False, str(error), Decimal("0.00")

    # =========================================================
    # PAYMENT - MAKE PAYMENT
    # =========================================================

    def make_payment(self, order_id, payment_method):
        try:
            order_id = self._positive_id(order_id, "Order ID")
            payment_method = self._required_text(
                payment_method, "Payment method"
            )
            if payment_method not in self.VALID_PAYMENT_METHODS:
                return False, "Payment method must be Cash, Card or QR."

            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    """
                    SELECT order_id, table_id, status, payment_status
                    FROM orders
                    WHERE order_id = %s
                    FOR UPDATE
                    """,
                    (order_id,),
                )
                order = cursor.fetchone()
                if order is None:
                    return self._failure(connection, "Order not found.")
                _, table_id, status, payment_status = order

                if status == "Cancelled":
                    return self._failure(
                        connection, "Cancelled orders cannot be paid."
                    )
                if status == "Completed" or payment_status == "Paid":
                    return self._failure(
                        connection, "This order has already been paid."
                    )
                if status != "Served":
                    return self._failure(
                        connection, "Only Served orders can be paid."
                    )

                # The order row is locked above. This check plus a unique
                # payment.order_id index (recommended in the migration notes)
                # protects against duplicate payment attempts.
                cursor.execute(
                    "SELECT COUNT(*) FROM payment WHERE order_id = %s",
                    (order_id,),
                )
                if cursor.fetchone()[0] > 0:
                    return self._failure(
                        connection,
                        "A payment record already exists for this order.",
                    )

                cursor.execute(
                    """
                    SELECT COUNT(*), COALESCE(SUM(subtotal), 0)
                    FROM order_item
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )
                item_count, total_amount = cursor.fetchone()
                total_amount = Decimal(str(total_amount or 0)).quantize(
                    self.MONEY_QUANTUM
                )
                if item_count == 0:
                    return self._failure(connection, "Order has no items.")
                if total_amount <= 0:
                    return self._failure(
                        connection, "Order total must be greater than zero."
                    )

                cursor.execute(
                    "UPDATE orders SET total_amount = %s WHERE order_id = %s",
                    (total_amount, order_id),
                )
                current_datetime = datetime.now()
                cursor.execute(
                    """
                    INSERT INTO payment
                        (order_id, amount, payment_method, payment_status, payment_date)
                    VALUES (%s, %s, %s, 'Paid', %s)
                    """,
                    (order_id, total_amount, payment_method, current_datetime),
                )
                payment_id = cursor.lastrowid

                cursor.execute(
                    """
                    UPDATE orders
                    SET status = 'Completed',
                        payment_status = 'Paid',
                        payment_method = %s
                    WHERE order_id = %s
                      AND status = 'Served'
                      AND COALESCE(payment_status, 'Pending') <> 'Paid'
                    """,
                    (payment_method, order_id),
                )
                if cursor.rowcount != 1:
                    return self._failure(
                        connection, "Order could not be completed."
                    )

                self._release_table_if_unused(cursor, table_id, order_id)
                connection.commit()
                return True, {
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "amount": total_amount,
                    "payment_method": payment_method,
                    "payment_status": "Paid",
                }
        except Exception as error:
            return False, str(error)

    # =========================================================
    # ORDER - GET SUMMARY
    # =========================================================

    def get_order_summary(self, order_id):
        order_id = self._positive_id(order_id, "Order ID")
        with self._db_cursor() as (_, cursor):
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
                FROM orders AS o
                JOIN customer AS c ON c.customer_id = o.customer_id
                LEFT JOIN cafe_table AS t ON t.table_id = o.table_id
                WHERE o.order_id = %s
                """,
                (order_id,),
            )
            order = cursor.fetchone()
            if order is None:
                return None

            cursor.execute(
                """
                SELECT
                    oi.product_id,
                    p.product_name,
                    oi.quantity,
                    oi.unit_price,
                    oi.subtotal
                FROM order_item AS oi
                JOIN product AS p ON p.product_id = oi.product_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """,
                (order_id,),
            )
            items = cursor.fetchall()
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
                "items": items,
            }

    # =========================================================
    # LEGACY POS CHECKOUT - KEPT FOR BACKWARD COMPATIBILITY
    # =========================================================

    def create_pos_order(self, customer_id, cart_items, payment_method):
        """Create a directly paid POS order for older callers.

        The newer Streamlit POS uses create_open_order() and make_payment().
        This legacy method is retained so the existing CLI/API does not break.
        """
        try:
            customer_id = self._positive_id(customer_id, "Customer ID")
            payment_method = self._required_text(
                payment_method, "Payment method"
            )
            if payment_method not in self.VALID_PAYMENT_METHODS:
                return False, "Invalid payment method.", Decimal("0.00")
            if not cart_items:
                return False, "Cart is empty.", Decimal("0.00")

            with self._db_cursor() as (connection, cursor):
                cursor.execute(
                    "SELECT customer_id FROM customer WHERE customer_id = %s",
                    (customer_id,),
                )
                if cursor.fetchone() is None:
                    return self._failure(
                        connection, "Customer not found.", Decimal("0.00")
                    )

                validated_items = []
                total_amount = Decimal("0.00")
                for item in cart_items:
                    if not isinstance(item, dict):
                        return self._failure(
                            connection,
                            "Each cart item must contain product_id and quantity.",
                            Decimal("0.00"),
                        )
                    product_id = self._positive_id(
                        item.get("product_id"), "Product ID"
                    )
                    quantity = self._quantity(item.get("quantity"))
                    cursor.execute(
                        """
                        SELECT product_name, price, availability
                        FROM product
                        WHERE product_id = %s
                        """,
                        (product_id,),
                    )
                    product = cursor.fetchone()
                    if product is None:
                        return self._failure(
                            connection,
                            f"Product ID {product_id} not found.",
                            Decimal("0.00"),
                        )
                    if not bool(product[2]):
                        return self._failure(
                            connection,
                            f"{product[0]} is not available.",
                            Decimal("0.00"),
                        )
                    unit_price = self._money(product[1])
                    subtotal = (unit_price * quantity).quantize(
                        self.MONEY_QUANTUM
                    )
                    total_amount += subtotal
                    validated_items.append(
                        (product_id, quantity, unit_price, subtotal)
                    )

                if total_amount <= 0:
                    return self._failure(
                        connection, "Order total must be greater than zero.", Decimal("0.00")
                    )

                now = datetime.now()
                cursor.execute(
                    """
                    INSERT INTO orders
                        (customer_id, user_id, order_date, order_time, status,
                         total_amount, payment_status, payment_method)
                    VALUES (%s, NULL, %s, %s, 'Completed', %s, 'Paid', %s)
                    """,
                    (
                        customer_id,
                        now.date(),
                        now.time().replace(microsecond=0),
                        total_amount,
                        payment_method,
                    ),
                )
                order_id = cursor.lastrowid
                for product_id, quantity, unit_price, subtotal in validated_items:
                    cursor.execute(
                        """
                        INSERT INTO order_item
                            (order_id, product_id, quantity, unit_price, subtotal)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (order_id, product_id, quantity, unit_price, subtotal),
                    )

                cursor.execute(
                    """
                    INSERT INTO payment
                        (order_id, amount, payment_method, payment_status, payment_date)
                    VALUES (%s, %s, %s, 'Paid', %s)
                    """,
                    (order_id, total_amount, payment_method, now),
                )
                connection.commit()
                return True, order_id, total_amount
        except Exception as error:
            return False, str(error), Decimal("0.00")

    # =========================================================
    # ORDER HISTORY - COMPLETED / CANCELLED ONLY
    # =========================================================

    def get_order_history(self):
        """Return historical records only; active orders stay in Open Orders."""
        with self._db_cursor(buffered=True) as (_, cursor):
            cursor.execute(
                """
                SELECT
                    o.order_id,
                    o.order_date,
                    o.order_time,
                    c.name AS customer_name,
                    o.status,
                    o.total_amount,
                    o.payment_method
                FROM orders AS o
                JOIN customer AS c ON c.customer_id = o.customer_id
                WHERE o.status IN ('Completed', 'Cancelled')
                ORDER BY o.order_id DESC
                """
            )
            return cursor.fetchall()