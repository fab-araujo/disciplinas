# Classe base
class Animal:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def exibir_informacoes(self):
        # Método genérico da classe base
        print(f"Animal: {self.nome}, {self.idade} anos")


# Classe Cachorro herdando de Animal
class Cachorro(Animal):
    def __init__(self, nome, idade, raca):
        # Chama o construtor da classe base
        super().__init__(nome, idade)
        self.raca = raca

    def exibir_informacoes(self):
        # Sobrescreve o método da classe base
        print(f"Cachorro: {self.nome}, {self.idade} anos, Raça: {self.raca}")


# Classe Gato herdando de Animal
class Gato(Animal):
    def __init__(self, nome, idade, cor):
        super().__init__(nome, idade)
        self.cor = cor

    def exibir_informacoes(self):
        print(f"Gato: {self.nome}, {self.idade} anos, Cor: {self.cor}")


# Programa principal
cachorro1 = Cachorro("Rex", 5, "Labrador")
gato1 = Gato("Mimi", 3, "Branca")

cachorro1.exibir_informacoes()  # Deve exibir: Cachorro: Rex, 5 anos, Raça: Labrador
gato1.exibir_informacoes()      # Deve exibir: Gato: Mimi, 3 anos, Cor: Branca


# Desafio extra: trabalhar com uma lista de animais
animais = [
    Cachorro("Bolt", 2, "Beagle"),
    Gato("Luna", 1, "Preta"),
    Cachorro("Max", 4, "Poodle")
]

for animal in animais:
    animal.exibir_informacoes()
