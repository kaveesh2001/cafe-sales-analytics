-- My Café SalesManager migration notes
-- Back up the database before running schema changes.

-- 1) Password hashing support
-- PBKDF2 password hashes need a column wide enough to hold the encoded hash.
-- Check the current column definition and NULL values first:
SHOW COLUMNS FROM users LIKE 'password';
SELECT COUNT(*) AS null_password_count
FROM users
WHERE password IS NULL;

-- Run this ALTER after confirming there are no NULL password values and
-- after taking a database backup. It is safe to rerun if the column is already
-- VARCHAR(255) NOT NULL, but MySQL may still rebuild the table.
ALTER TABLE users
MODIFY COLUMN password VARCHAR(255) NOT NULL;

-- 2) One payment per order (recommended database-level duplicate protection)
-- First inspect existing duplicates:
SELECT order_id, COUNT(*) AS payment_count
FROM payment
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Only when the query above returns no rows, and only if this unique key does
-- not already exist, run the following statement once:
-- ALTER TABLE payment
-- ADD CONSTRAINT uq_payment_order_id UNIQUE (order_id);

-- 3) Transactions and row locks require transactional table engines.
-- Check the storage engines used by the application's tables:
SELECT TABLE_NAME, ENGINE
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN (
      'product', 'customer', 'users', 'cafe_table',
      'orders', 'order_item', 'payment'
  );

-- If any of these tables are not InnoDB, back up first and convert them using:
-- ALTER TABLE table_name ENGINE = InnoDB;
