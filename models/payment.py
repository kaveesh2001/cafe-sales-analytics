class Payment:
    def __init__(
        self,
        payment_id,
        order_id,
        amount,
        payment_method,
        payment_status,
        payment_date
    ):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.payment_date = payment_date

    def get_details(self):
        return (
            f"Payment ID: {self.payment_id}, "
            f"Order ID: {self.order_id}, "
            f"Amount: {self.amount}, "
            f"Payment Method: {self.payment_method}, "
            f"Payment Status: {self.payment_status}, "
            f"Payment Date: {self.payment_date}"
        )