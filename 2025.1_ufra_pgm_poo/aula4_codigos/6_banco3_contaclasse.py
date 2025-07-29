class Conta():
    def __init__(self):
        self.nome = ""
        self.saldo = 0
        self.senha = ""

    def dadosConta(self):
        print('Dados da conta:')
        print('       Nome:', self.nome)
        print('       Saldo:', self.saldo)
        print('       Senha:', self.senha)
        print()

conta = Conta()
conta.dadosConta()