class Product:
    def __init__(
        self,
        product_id,
        product_name,
        category,
        price,
        availability=True,
        image_url=None
    ):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.price = price
        self.availability = availability
        self.image_url = image_url

    def get_details(self):
        return (
            f"ID: {self.product_id}, "
            f"Name: {self.product_name}, "
            f"Category: {self.category}, "
            f"Price: {self.price}, "
            f"Available: {self.availability}, "
            f"Image URL: {self.image_url}"
        )