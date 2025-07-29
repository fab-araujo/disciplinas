class Conta():
    def __init__(self, nome, saldo, senha):
        self.nome = nome
        self.saldo = saldo
        self.senha = senha

    def dadosConta(self):
        print('Dados da conta:')
        print('       Nome:', self.nome)
        print('       Saldo:', self.saldo)
        print('       Senha:', self.senha)
        print()

    def verSaldo(self, senha):
        if senha != self.senha:
            print('Senha incorreta!')
        else:
            print('Seu saldo é:', self.saldo)

conta = Conta("Joe", 100, "minhasenha")
conta.dadosConta()
conta.verSaldo("minhasenha")