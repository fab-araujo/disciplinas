from models.entities import LibraryEntity

class Item(LibraryEntity):
    def __init__(self, name):
        super().__init__(name)

class Book(Item):
    def __init__(self, name, author, isbn):
        super().__init__(name)
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return f"Livro: {self.name} - Autor: {self.author} - ISBN: {self.isbn}"

    def update_status(self, new_status):
        self.status = new_status

    def validate(self):
        return bool(self.isbn)

    def serialize(self):
        return {"type": "Book", "name": self.name, "author": self.author, "isbn": self.isbn}

class Magazine(Item):
    def __init__(self, name, edition):
        super().__init__(name)
        self.edition = edition

    def display_info(self):
        return f"Revista: {self.name} - Edição: {self.edition}"

    def update_status(self, new_status):
        self.status = new_status

    def validate(self):
        return bool(self.edition)

    def serialize(self):
        return {"type": "Magazine", "name": self.name, "edition": self.edition}

class DVD(Item):
    def __init__(self, name, duration):
        super().__init__(name)
        self.duration = duration

    def display_info(self):
        return f"DVD: {self.name} - Duração: {self.duration}"

    def update_status(self, new_status):
        self.status = new_status

    def validate(self):
        return bool(self.duration)

    def serialize(self):
        return {"type": "DVD", "name": self.name, "duration": self.duration}
