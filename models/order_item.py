class OrderItem:
    def __init__(
        self,
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        subtotal
    ):
        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal

    def get_details(self):
        return (
            f"Order Item ID: {self.order_item_id}, "
            f"Order ID: {self.order_id}, "
            f"Product ID: {self.product_id}, "
            f"Quantity: {self.quantity}, "
            f"Unit Price: {self.unit_price}, "
            f"Subtotal: {self.subtotal}"
        )