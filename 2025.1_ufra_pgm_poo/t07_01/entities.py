"""
Entidades de domínio da biblioteca.

Este módulo demonstra conceitos de POO:
- Abstração: classes e métodos abstratos (LibraryEntity, Transaction)
- Herança: Book/Magazine <- Item <- LibraryEntity; Student/Professor <- User <- LibraryEntity
- Polimorfismo: display_info/process variam conforme a subclasse
- Encapsulamento: atributos privados com acesso controlado via properties
"""

from abc import ABC, abstractmethod
from datetime import datetime

class LibraryEntity(ABC):
    """Classe base abstrata para todas as entidades da biblioteca."""
    def __init__(self, id, name):
        self.__id = id
        self.__name = name
        self.__created_at = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self.__name = value

    @abstractmethod
    def display_info(self):
        """Retorna uma string legível com informações para a interface."""
        pass

    @abstractmethod
    def update_status(self, new_status):
        """Atualiza o estado interno da entidade (contrato a ser definido nas subclasses)."""
        pass

    @abstractmethod
    def validate(self):
        """Valida se a entidade pode participar de uma operação (ex.: empréstimo)."""
        pass

    @abstractmethod
    def serialize(self):
        """Retorna um dicionário serializável em JSON com os dados essenciais."""
        pass

class Item(LibraryEntity):
    """Representa um item emprestável (livro, revista, etc.)."""
    def __init__(self, id, name, category):
        super().__init__(id, name)
        self.__status = "available"
        self.__category = category

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in ["available", "borrowed"]:
            raise ValueError("Invalid status")
        self.__status = value

    def update_status(self, new_status):
        self.status = new_status

    def validate(self):
        # Um item só pode ser emprestado se estiver disponível
        return self.__status == "available"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.__category,
            "status": self.__status
        }

class Book(Item):
    """Livro com autor e ISBN."""
    def __init__(self, id, name, author, isbn):
        super().__init__(id, name, "book")
        self.__author = author
        self.__isbn = isbn

    def display_info(self):
        return f"Book: {self.name} by {self.__author} (ISBN: {self.__isbn}) - Status: {self.status}"

    def serialize(self):
        base = super().serialize()
        base.update({"author": self.__author, "isbn": self.__isbn, "type": "book"})
        return base

class Magazine(Item):
    """Revista com edição."""
    def __init__(self, id, name, edition):
        super().__init__(id, name, "magazine")
        self.__edition = edition

    def display_info(self):
        return f"Magazine: {self.name}, Edition {self.__edition} - Status: {self.status}"

    def serialize(self):
        base = super().serialize()
        base.update({"edition": self.__edition, "type": "magazine"})
        return base

class User(LibraryEntity):
    """Usuário da biblioteca (abstrato)."""
    def __init__(self, id, name, user_type):
        super().__init__(id, name)
        self.__user_type = user_type
        self.__borrowed_items = []
        self.__status = "active"

    @property
    def borrowed_items(self):
        return self.__borrowed_items


    def update_status(self, new_status):
        # Basic user status tracking; can be extended (e.g., suspended, banned)
        if not isinstance(new_status, str) or not new_status.strip():
            raise ValueError("Invalid status")
        self.__status = new_status.strip()

    def borrow_item(self, item):
        if len(self.__borrowed_items) >= self._max_borrow_limit():
            raise ValueError(f"{self.__user_type} cannot borrow more items")
        self.__borrowed_items.append(item)

    def return_item(self, item):
        if item in self.__borrowed_items:
            self.__borrowed_items.remove(item)

    @abstractmethod
    def _max_borrow_limit(self):
        pass

    def validate(self):
        # Usuário só pode pegar mais itens se não atingiu o limite
        return len(self.__borrowed_items) < self._max_borrow_limit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_type": self.__user_type,
            "borrowed_items": [item.id for item in self.__borrowed_items],
            "status": self.__status
        }

class Student(User):
    """Aluno com limite de 3 itens."""
    def __init__(self, id, name):
        super().__init__(id, name, "student")

    def _max_borrow_limit(self):
        return 3

    def display_info(self):
        return f"Student: {self.name} (ID: {self.id}) - Borrowed: {len(self.borrowed_items)} items"

class Professor(User):
    """Professor com limite de 10 itens."""
    def __init__(self, id, name):
        super().__init__(id, name, "professor")

    def _max_borrow_limit(self):
        return 10

    def display_info(self):
        return f"Professor: {self.name} (ID: {self.id}) - Borrowed: {len(self.borrowed_items)} items"

class Transaction(LibraryEntity):
    """Transação abstrata entre um usuário e um item (empréstimo/devolução)."""
    def __init__(self, id, user, item):
        super().__init__(id, f"Transaction {id}")
        self.__user = user
        self.__item = item
        self.__date = datetime.now()
        self.__status = "pending"

    @property
    def user(self):
        return self.__user

    @property
    def item(self):
        return self.__item

    def validate(self):
        # Só é válida se o usuário puder pegar e o item estiver disponível
        return self.__user.validate() and self.__item.validate()

    @abstractmethod
    def process(self):
        pass

    # Sem cálculo de multa/prazo: removido do sistema

    def update_status(self, new_status):
        self.__status = new_status

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.__user.id,
            "item_id": self.__item.id,
            "date": self.__date.isoformat(),
            "status": self.__status,
            "type": self.__class__.__name__
        }

    @property
    def status(self):
        return self.__status

class Loan(Transaction):
    """Empréstimo de item ao usuário."""
    def __init__(self, id, user, item):
        super().__init__(id, user, item)

    def process(self):
        if not self.validate():
            raise ValueError("Invalid loan conditions")
        self.item.update_status("borrowed")
        self.user.borrow_item(self.item)
        self.update_status("completed")

    def display_info(self):
        return f"Loan: {self.item.name} to {self.user.name} - Status: {self.status}"

class Return(Transaction):
    """Devolução de item por um usuário."""
    def __init__(self, id, user, item):
        super().__init__(id, user, item)

    def process(self):
        if self.item not in self.user.borrowed_items:
            raise ValueError("Item not borrowed by user")
        self.item.update_status("available")
        self.user.return_item(self.item)
        self.update_status("completed")

    def display_info(self):
        return f"Return: {self.item.name} by {self.user.name} - Status: {self.status}"