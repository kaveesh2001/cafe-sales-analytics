-- My Cafe menu + image support
-- Run this script against the same database used by your project.

-- Add image_url only when it does not already exist.
SET @add_image_sql = (SELECT IF(COUNT(*) = 0, 'ALTER TABLE product ADD COLUMN image_url VARCHAR(500) NULL AFTER availability', 'SELECT 1') FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'product' AND COLUMN_NAME = 'image_url');
PREPARE add_image_stmt FROM @add_image_sql;
EXECUTE add_image_stmt;
DEALLOCATE PREPARE add_image_stmt;

-- Add new menu rows without deleting existing products.
INSERT INTO product (product_name, category, price, availability, image_url)
SELECT menu.product_name, menu.category, menu.price, TRUE, menu.image_url
FROM (
    SELECT 'Espresso', 'Hot Coffee', 450, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Americano', 'Hot Coffee', 500, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cappuccino', 'Hot Coffee', 650, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Café Latte', 'Hot Coffee', 650, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Café Mocha', 'Hot Coffee', 700, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Flat White', 'Hot Coffee', 650, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Caramel Macchiato', 'Hot Coffee', 750, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Vanilla Latte', 'Hot Coffee', 700, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Hazelnut Latte', 'Hot Coffee', 700, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Americano', 'Cold Coffee', 550, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Latte', 'Cold Coffee', 700, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Mocha', 'Cold Coffee', 750, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Caramel Latte', 'Cold Coffee', 750, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Vanilla Latte', 'Cold Coffee', 750, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Iced Coffee', 'Cold Coffee', 600, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cold Brew Coffee', 'Cold Coffee', 700, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Coffee Frappe', 'Frappes & Shakes', 800, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Frappe', 'Frappes & Shakes', 750, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Caramel Frappe', 'Frappes & Shakes', 800, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Vanilla Frappe', 'Frappes & Shakes', 750, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Milkshake', 'Frappes & Shakes', 700, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Strawberry Milkshake', 'Frappes & Shakes', 700, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Vanilla Milkshake', 'Frappes & Shakes', 650, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Mango Milkshake', 'Frappes & Shakes', 700, 'https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Ceylon Tea', 'Tea & Other Hot Drinks', 350, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'English Breakfast Tea', 'Tea & Other Hot Drinks', 400, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Green Tea', 'Tea & Other Hot Drinks', 450, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Earl Grey Tea', 'Tea & Other Hot Drinks', 450, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Ginger Tea', 'Tea & Other Hot Drinks', 450, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Lemon Tea', 'Tea & Other Hot Drinks', 400, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Hot Chocolate', 'Tea & Other Hot Drinks', 600, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chai Latte', 'Tea & Other Hot Drinks', 550, 'https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Sandwich', 'Sandwiches', 750, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken & Cheese Sandwich', 'Sandwiches', 850, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Tuna Sandwich', 'Sandwiches', 750, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Egg Salad Sandwich', 'Sandwiches', 650, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cheese & Tomato Sandwich', 'Sandwiches', 650, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Club Sandwich', 'Sandwiches', 950, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Smoked Chicken Sandwich', 'Sandwiches', 850, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Mayo Sandwich', 'Sandwiches', 800, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cream Cheese Bagel', 'Bagels', 600, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Bagel', 'Bagels', 800, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken & Cheese Bagel', 'Bagels', 850, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Tuna Bagel', 'Bagels', 800, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Smoked Chicken Bagel', 'Bagels', 850, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Egg Salad Bagel', 'Bagels', 700, 'https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Plain Croissant', 'Croissant & Bakery', 450, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Croissant', 'Croissant & Bakery', 550, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Butter Croissant', 'Croissant & Bakery', 500, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken & Cheese Croissant', 'Croissant & Bakery', 850, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Smoked Chicken Croissant', 'Croissant & Bakery', 850, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Tuna & Cucumber Croissant', 'Croissant & Bakery', 800, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Egg Salad Croissant', 'Croissant & Bakery', 700, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cheese & Tomato Croissant', 'Croissant & Bakery', 700, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Muffin', 'Croissant & Bakery', 450, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Blueberry Muffin', 'Croissant & Bakery', 500, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Banana Muffin', 'Croissant & Bakery', 450, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Chip Cookie', 'Croissant & Bakery', 350, 'https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Fish Bun', 'Sri Lankan Short Eats', 300, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chicken Bun', 'Sri Lankan Short Eats', 350, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Egg Bun', 'Sri Lankan Short Eats', 250, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Fish Patty', 'Sri Lankan Short Eats', 300, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chicken Patty', 'Sri Lankan Short Eats', 350, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Vegetable Patty', 'Sri Lankan Short Eats', 250, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Fish Roti', 'Sri Lankan Short Eats', 350, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chicken Roti', 'Sri Lankan Short Eats', 400, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Fish Cutlet', 'Sri Lankan Short Eats', 250, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chicken Cutlet', 'Sri Lankan Short Eats', 300, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chinese Roll', 'Sri Lankan Short Eats', 300, 'https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg'
    UNION ALL SELECT 'Chicken Fried Rice', 'Main Meals', 900, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Vegetable Fried Rice', 'Main Meals', 750, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Egg Fried Rice', 'Main Meals', 800, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Noodles', 'Main Meals', 900, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Vegetable Noodles', 'Main Meals', 750, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Pasta', 'Main Meals', 950, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Lasagna', 'Main Meals', 1000, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chicken Rice Bowl', 'Main Meals', 950, 'https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Cake', 'Desserts & Sweet Bakery', 650, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Red Velvet Cake', 'Desserts & Sweet Bakery', 700, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cheesecake', 'Desserts & Sweet Bakery', 750, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Blueberry Cheesecake', 'Desserts & Sweet Bakery', 750, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Brownie', 'Desserts & Sweet Bakery', 500, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Brownie Cheesecake', 'Desserts & Sweet Bakery', 700, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Tiramisu', 'Desserts & Sweet Bakery', 750, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Chocolate Lava Cake', 'Desserts & Sweet Bakery', 800, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Carrot Cake', 'Desserts & Sweet Bakery', 600, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Doughnut', 'Desserts & Sweet Bakery', 400, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Cinnamon Roll', 'Desserts & Sweet Bakery', 550, 'https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Orange Juice', 'Fresh Juices & Smoothies', 550, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Watermelon Juice', 'Fresh Juices & Smoothies', 450, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Pineapple Juice', 'Fresh Juices & Smoothies', 500, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Mango Juice', 'Fresh Juices & Smoothies', 550, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Passion Fruit Juice', 'Fresh Juices & Smoothies', 550, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Mixed Fruit Juice', 'Fresh Juices & Smoothies', 650, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Lime Juice', 'Fresh Juices & Smoothies', 400, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Avocado Smoothie', 'Fresh Juices & Smoothies', 650, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'Banana Smoothie', 'Fresh Juices & Smoothies', 600, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85'
    UNION ALL SELECT 'King Coconut', 'Sri Lankan Drinks', 400, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'King Coconut & Lime', 'Sri Lankan Drinks', 500, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'Wood Apple Juice', 'Sri Lankan Drinks', 500, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'Avocado Milkshake', 'Sri Lankan Drinks', 650, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'Kola Kenda', 'Sri Lankan Drinks', 400, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'Koththamalli', 'Sri Lankan Drinks', 400, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
    UNION ALL SELECT 'Belimal', 'Sri Lankan Drinks', 350, 'https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg'
) AS menu
LEFT JOIN product existing ON existing.product_name = menu.product_name
WHERE existing.product_id IS NULL;

-- Refresh images/category/price for products with the same names if they already exist.
UPDATE product SET category='Hot Coffee', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Espresso';
UPDATE product SET category='Hot Coffee', price=500, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Americano';
UPDATE product SET category='Hot Coffee', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cappuccino';
UPDATE product SET category='Hot Coffee', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Café Latte';
UPDATE product SET category='Hot Coffee', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Café Mocha';
UPDATE product SET category='Hot Coffee', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Flat White';
UPDATE product SET category='Hot Coffee', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Caramel Macchiato';
UPDATE product SET category='Hot Coffee', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Vanilla Latte';
UPDATE product SET category='Hot Coffee', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Hazelnut Latte';
UPDATE product SET category='Cold Coffee', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Americano';
UPDATE product SET category='Cold Coffee', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Latte';
UPDATE product SET category='Cold Coffee', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Mocha';
UPDATE product SET category='Cold Coffee', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Caramel Latte';
UPDATE product SET category='Cold Coffee', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Vanilla Latte';
UPDATE product SET category='Cold Coffee', price=600, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Iced Coffee';
UPDATE product SET category='Cold Coffee', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cold Brew Coffee';
UPDATE product SET category='Frappes & Shakes', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Coffee Frappe';
UPDATE product SET category='Frappes & Shakes', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Frappe';
UPDATE product SET category='Frappes & Shakes', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Caramel Frappe';
UPDATE product SET category='Frappes & Shakes', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Vanilla Frappe';
UPDATE product SET category='Frappes & Shakes', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Milkshake';
UPDATE product SET category='Frappes & Shakes', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Strawberry Milkshake';
UPDATE product SET category='Frappes & Shakes', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Vanilla Milkshake';
UPDATE product SET category='Frappes & Shakes', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1584649258298-7ecf2437f769?auto=format&fit=crop&w=900&q=85' WHERE product_name='Mango Milkshake';
UPDATE product SET category='Tea & Other Hot Drinks', price=350, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Ceylon Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=400, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='English Breakfast Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Green Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Earl Grey Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Ginger Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=400, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Lemon Tea';
UPDATE product SET category='Tea & Other Hot Drinks', price=600, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Hot Chocolate';
UPDATE product SET category='Tea & Other Hot Drinks', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1525629545813-e4e7ba89e506?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chai Latte';
UPDATE product SET category='Sandwiches', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Sandwich';
UPDATE product SET category='Sandwiches', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken & Cheese Sandwich';
UPDATE product SET category='Sandwiches', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Tuna Sandwich';
UPDATE product SET category='Sandwiches', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Egg Salad Sandwich';
UPDATE product SET category='Sandwiches', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cheese & Tomato Sandwich';
UPDATE product SET category='Sandwiches', price=950, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Club Sandwich';
UPDATE product SET category='Sandwiches', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Smoked Chicken Sandwich';
UPDATE product SET category='Sandwiches', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Mayo Sandwich';
UPDATE product SET category='Bagels', price=600, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cream Cheese Bagel';
UPDATE product SET category='Bagels', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Bagel';
UPDATE product SET category='Bagels', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken & Cheese Bagel';
UPDATE product SET category='Bagels', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Tuna Bagel';
UPDATE product SET category='Bagels', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Smoked Chicken Bagel';
UPDATE product SET category='Bagels', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1681477526380-fc3bca2bad72?auto=format&fit=crop&w=900&q=85' WHERE product_name='Egg Salad Bagel';
UPDATE product SET category='Croissant & Bakery', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Plain Croissant';
UPDATE product SET category='Croissant & Bakery', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Croissant';
UPDATE product SET category='Croissant & Bakery', price=500, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Butter Croissant';
UPDATE product SET category='Croissant & Bakery', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken & Cheese Croissant';
UPDATE product SET category='Croissant & Bakery', price=850, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Smoked Chicken Croissant';
UPDATE product SET category='Croissant & Bakery', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Tuna & Cucumber Croissant';
UPDATE product SET category='Croissant & Bakery', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Egg Salad Croissant';
UPDATE product SET category='Croissant & Bakery', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cheese & Tomato Croissant';
UPDATE product SET category='Croissant & Bakery', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Muffin';
UPDATE product SET category='Croissant & Bakery', price=500, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Blueberry Muffin';
UPDATE product SET category='Croissant & Bakery', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Banana Muffin';
UPDATE product SET category='Croissant & Bakery', price=350, availability=TRUE, image_url='https://images.unsplash.com/photo-1754652327649-b7f96de797bd?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Chip Cookie';
UPDATE product SET category='Sri Lankan Short Eats', price=300, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Fish Bun';
UPDATE product SET category='Sri Lankan Short Eats', price=350, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Chicken Bun';
UPDATE product SET category='Sri Lankan Short Eats', price=250, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Egg Bun';
UPDATE product SET category='Sri Lankan Short Eats', price=300, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Fish Patty';
UPDATE product SET category='Sri Lankan Short Eats', price=350, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Chicken Patty';
UPDATE product SET category='Sri Lankan Short Eats', price=250, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Vegetable Patty';
UPDATE product SET category='Sri Lankan Short Eats', price=350, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Fish Roti';
UPDATE product SET category='Sri Lankan Short Eats', price=400, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Chicken Roti';
UPDATE product SET category='Sri Lankan Short Eats', price=250, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Fish Cutlet';
UPDATE product SET category='Sri Lankan Short Eats', price=300, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Chicken Cutlet';
UPDATE product SET category='Sri Lankan Short Eats', price=300, availability=TRUE, image_url='https://static.wixstatic.com/media/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg/v1/fill/w_1000,h_750,al_c,q_85,usm_0.66_1.00_0.01/ed7e93_03bd50de01be46afb8076b11cc55d56f~mv2.jpg' WHERE product_name='Chinese Roll';
UPDATE product SET category='Main Meals', price=900, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Fried Rice';
UPDATE product SET category='Main Meals', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Vegetable Fried Rice';
UPDATE product SET category='Main Meals', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Egg Fried Rice';
UPDATE product SET category='Main Meals', price=900, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Noodles';
UPDATE product SET category='Main Meals', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Vegetable Noodles';
UPDATE product SET category='Main Meals', price=950, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Pasta';
UPDATE product SET category='Main Meals', price=1000, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Lasagna';
UPDATE product SET category='Main Meals', price=950, availability=TRUE, image_url='https://images.unsplash.com/photo-1669109230787-71bdd4699af4?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chicken Rice Bowl';
UPDATE product SET category='Desserts & Sweet Bakery', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Cake';
UPDATE product SET category='Desserts & Sweet Bakery', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Red Velvet Cake';
UPDATE product SET category='Desserts & Sweet Bakery', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cheesecake';
UPDATE product SET category='Desserts & Sweet Bakery', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Blueberry Cheesecake';
UPDATE product SET category='Desserts & Sweet Bakery', price=500, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Brownie';
UPDATE product SET category='Desserts & Sweet Bakery', price=700, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Brownie Cheesecake';
UPDATE product SET category='Desserts & Sweet Bakery', price=750, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Tiramisu';
UPDATE product SET category='Desserts & Sweet Bakery', price=800, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Chocolate Lava Cake';
UPDATE product SET category='Desserts & Sweet Bakery', price=600, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Carrot Cake';
UPDATE product SET category='Desserts & Sweet Bakery', price=400, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Doughnut';
UPDATE product SET category='Desserts & Sweet Bakery', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1681725271035-7270a7464f5b?auto=format&fit=crop&w=900&q=85' WHERE product_name='Cinnamon Roll';
UPDATE product SET category='Fresh Juices & Smoothies', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Orange Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=450, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Watermelon Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=500, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Pineapple Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Mango Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=550, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Passion Fruit Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Mixed Fruit Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=400, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Lime Juice';
UPDATE product SET category='Fresh Juices & Smoothies', price=650, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Avocado Smoothie';
UPDATE product SET category='Fresh Juices & Smoothies', price=600, availability=TRUE, image_url='https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&w=900&q=85' WHERE product_name='Banana Smoothie';
UPDATE product SET category='Sri Lankan Drinks', price=400, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='King Coconut';
UPDATE product SET category='Sri Lankan Drinks', price=500, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='King Coconut & Lime';
UPDATE product SET category='Sri Lankan Drinks', price=500, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='Wood Apple Juice';
UPDATE product SET category='Sri Lankan Drinks', price=650, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='Avocado Milkshake';
UPDATE product SET category='Sri Lankan Drinks', price=400, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='Kola Kenda';
UPDATE product SET category='Sri Lankan Drinks', price=400, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='Koththamalli';
UPDATE product SET category='Sri Lankan Drinks', price=350, availability=TRUE, image_url='https://trippingsrilanka.com/wp-content/uploads/2024/05/download.jpeg' WHERE product_name='Belimal';
