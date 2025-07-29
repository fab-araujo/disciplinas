"""
Factory Method Design Pattern

Intenção: Fornece uma interface para criar objetos em uma superclasse, mas permite que
as subclasses alterem o tipo de objetos que serão criados.
"""


from __future__ import annotations
from abc import ABC, abstractmethod


class Creator(ABC):
    """
    A classe Creator declara o método fábrica que deve retornar um
    objeto de uma classe Product. As subclasses da Creator geralmente fornecem a
    implementação deste método.
    """

    @abstractmethod
    def createProduct(self): #factory method (método fábrica)
        """
        Observe que o Criador também pode fornecer alguma implementação padrão do
        método fábrica.
        """
        pass

    def someOperation(self) -> str:
        """
        Observe também que, apesar do nome, a principal responsabilidade de Creator
        não é criar produtos. Normalmente, ele contém alguma lógica de negócios central
        que se baseia em objetos Product, retornados pelo método fábrica.
        Subclasses podem alterar indiretamente essa lógica de negócios, sobrescrevendo o
        método fábrica e retornando um tipo diferente de produto a partir dele.
        """

        # Call the factory method to create a Product object.
        product = self.createProduct()

        # Now, use the product.
        result = f"Creator: O mesmo código de creator acabou de funcionar com {product.doStuff()}"

        return result


"""
Os Croncrete Creators (Criadores Concretos) substituem o método fábrica para alterar o tipo do produto
resultante.
"""


class ConcreteCreatorA(Creator):
    """
    Observe que a assinatura do método ainda usa o tipo abstrato do produto,
    mesmo que o produto concreto seja retornado pelo método. Dessa
    forma, o Creator pode permanecer independente das classes concretas do produto.
    """

    def createProduct(self) -> Product: #factory method (método fábrica)
        return ConcreteProductA()


class ConcreteCreatorB(Creator):
    def createProduct(self) -> Product: #factory method (método fábrica)
        return ConcreteProductB()


class Product(ABC):
    """
    A interface Product declara as operações que todos os produtos concretos
    devem implementar.
    """

    @abstractmethod
    def doStuff(self) -> str:
        pass


"""
Os Concrete Products (Produtos Concretos) fornecem várias implementações da interface do produto.
"""


class ConcreteProductA(Product):
    def doStuff(self) -> str:
        return "{Resultado do ConcreteProductA}"


class ConcreteProductB(Product):
    def doStuff(self) -> str:
        return "{Resultado do ConcreteProductB}"


def client_code(creator: Creator) -> None:
    """
    O código do cliente trabalha com uma instância de um criador concreto, embora por meio
    de sua interface base. Enquanto o cliente continuar trabalhando com o criador por meio
    da interface base, você pode passar a ele qualquer subclasse do criador.
    """

    print(f"Cliente: Não sei qual é a classe do criador, mas ainda funciona.\n"
          f"{creator.someOperation()}", end="")


if __name__ == "__main__":
    print("Aplicativo: lançado com o ConcreteCreatorA.")
    client_code(ConcreteCreatorA())
    print("\n")

    print("Aplicativo: lançado com o ConcreteCreatorB.")
    client_code(ConcreteCreatorB())
