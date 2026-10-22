class User:
    def __init__(self, user_id, name, username, password, role):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def get_details(self):
        return (
            f"ID: {self.user_id}, "
            f"Name: {self.name}, "
            f"Username: {self.username}, "
            f"Role: {self.role}"
        )