import abc
from models.entities import LibraryEntity

class Transaction(LibraryEntity, abc.ABC):
    def __init__(self, name):
        super().__init__(name)

    @abc.abstractmethod
    def process(self, user, item):
        pass

class Loan(Transaction):
    def display_info(self):
        return "Empréstimo"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Loan"}

    def process(self, user, item):
        if user.limit > 0 and item.status == "available":
            item.status = "borrowed"
            user.limit -= 1
            return True
        return False

class Return(Transaction):
    def display_info(self):
        return "Devolução"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Return"}

    def process(self, user, item):
        item.status = "available"
        user.limit += 1
        return True

class Reservation(Transaction):
    def display_info(self):
        return "Reserva"

    def update_status(self, new_status):
        pass

    def validate(self):
        return True

    def serialize(self):
        return {"type": "Reservation"}

    def process(self, user, item):
        return f"Item {item.name} reservado por {user.name}"
