class CafeTable:
    def __init__(
        self,
        table_id,
        table_number,
        capacity,
        status
    ):
        self.table_id = table_id
        self.table_number = table_number
        self.capacity = capacity
        self.status = status

    def get_details(self):
        return (
            f"Table ID: {self.table_id}, "
            f"Table Number: {self.table_number}, "
            f"Capacity: {self.capacity}, "
            f"Status: {self.status}"
        )