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

    def depositar(self, valor, senha):
        if valor < 0:
            print('Você não pode depositar um valor negativo!')
        elif senha != self.senha:
            print('Senha incorreta!')
        else:
            self.saldo += valor
            print('Seu novo saldo é:', self.saldo)

    def sacar(self, valor, senha):
        if valor < 0:
            print('Você não pode sacar um valor negativo!')
        elif senha != self.senha:
            print('Senha incorreta!')
        elif valor > self.saldo:
            print('Você não pode sacar mais do que o seu saldo!')
        else:
            self.saldo -= valor
            print('Seu novo saldo é:', self.saldo)


conta = Conta("Joe", 100, "minhasenha")

while True:
    print()
    print('Aperte b para ver o saldo')
    print('Aperte d para fazer um depósito')
    print('Aperte w para fazer um saque')
    print('Aperte s para ver os dados da conta')
    print('Aperte q para sair')
    print()

    acao = input('O que você quer fazer? (b/d/w/s/q): ')
    acao = acao.lower()  # force lowercase
    acao = acao[0]  # just use first letter
    print()
    
    if acao == 'b':
        print('Ver saldo:')
        senha = input('Digite sua senha: ')
        saldo = conta.verSaldo(senha)       

    elif acao == 'd':
        print('Depositar:')
        valorDepositado = input('Digite o valor que será depositado: ')
        valorDepositado = int(valorDepositado)
        senha = input('Digite sua senha: ')
        conta.depositar(valorDepositado, senha)  

    elif acao == 's':  # show
        conta.dadosConta()

    elif acao == 'q':
        break

    elif acao == 'w':
        print('Saque:')

        valorSacado = input('Digite o valor do saque: ')
        valorSacado = int(valorSacado)
        senha = input('Digite sua senha: ')
        conta.sacar(valorSacado, senha)

print('Fim do programa!')