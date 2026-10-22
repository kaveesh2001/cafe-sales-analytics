class Order:

    def __init__(
        self,
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
    ):

        self.order_id = order_id
        self.customer_id = customer_id
        self.user_id = user_id
        self.table_id = table_id
        self.order_date = order_date
        self.order_time = order_time
        self.status = status
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.payment_method = payment_method


    def get_details(self):

        return (
            f"Order ID: {self.order_id}, "
            f"Customer ID: {self.customer_id}, "
            f"User ID: {self.user_id}, "
            f"Table ID: {self.table_id}, "
            f"Date: {self.order_date}, "
            f"Time: {self.order_time}, "
            f"Status: {self.status}, "
            f"Total: {self.total_amount}, "
            f"Payment Status: {self.payment_status}, "
            f"Payment Method: {self.payment_method}"
        )


    def __str__(self):

        return (
            f"Order ID: {self.order_id}, "
            f"Customer ID: {self.customer_id}, "
            f"User ID: {self.user_id}, "
            f"Table ID: {self.table_id}, "
            f"Date: {self.order_date}, "
            f"Time: {self.order_time}, "
            f"Status: {self.status}, "
            f"Total: {self.total_amount}, "
            f"Payment Status: {self.payment_status}, "
            f"Payment Method: {self.payment_method}"
        )