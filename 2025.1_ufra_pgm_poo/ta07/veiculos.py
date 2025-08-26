# pessoas.py
from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, nome, idade):
        self.__nome = nome
        self.__idade = idade

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, valor):
        self.__idade = valor

    @abstractmethod
    def exibir_informacoes(self):
        pass

    @abstractmethod
    def acao_especial(self):
        pass

class Aluno(Pessoa):
    def __init__(self, nome, idade, matricula, curso):
        super().__init__(nome, idade)
        self.__matricula = matricula
        self.__curso = curso

    @property
    def matricula(self):
        return self.__matricula

    @property
    def curso(self):
        return self.__curso

    def exibir_informacoes(self):
        return f"{self.nome} | {s
