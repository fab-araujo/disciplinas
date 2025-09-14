from models.entities import LibraryEntity

class User(LibraryEntity):
    def __init__(self, name, limit):
        super().__init__(name)
        self.limit = limit

class Student(User):
    def __init__(self, name):
        super().__init__(name, limit=3)

    def display_info(self):
        return f"Estudante: {self.name} - Limite: {self.limit}"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Student", "name": self.name, "limit": self.limit}

class Professor(User):
    def __init__(self, name):
        super().__init__(name, limit=999)

    def display_info(self):
        return f"Professor: {self.name} - Acesso ilimitado"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Professor", "name": self.name, "limit": self.limit}

class Visitor(User):
    def __init__(self, name):
        super().__init__(name, limit=1)

    def display_info(self):
        return f"Visitante: {self.name} - Limite: {self.limit}"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Visitor", "name": self.name, "limit": self.limit}
