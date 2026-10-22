class Customer:
    def __init__(self, customer_id, name, phone,):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        

    def get_details(self):
        return (
            f"ID: {self.customer_id}, "
            f"Name: {self.name}, "
            f"Phone: {self.phone}, "
           
        )