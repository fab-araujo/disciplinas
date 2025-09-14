import abc
from datetime import datetime

class LibraryEntity(abc.ABC):
    _next_id = 1
    def __init__(self, name):
        self.__id = LibraryEntity._next_id
        LibraryEntity._next_id += 1
        self.name = name
        self.created_at = datetime.now()
        self.__status = "available"

    @property
    def id(self):
        return self.__id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value in ["available", "borrowed"]:
            self.__status = value
        else:
            raise ValueError("Status inválido.")

    @abc.abstractmethod
    def display_info(self):
        pass

    @abc.abstractmethod
    def update_status(self, new_status):
        pass

    @abc.abstractmethod
    def validate(self):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass
