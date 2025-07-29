contaNome = ''
contaSaldo = 0
contaSenha = ''

def novaConta(nome, saldo, senha):
    global contaNome, contaSaldo, contaSenha
    contaNome = nome
    contaSaldo = saldo
    contaSenha = senha

def dadosConta():
    global contaNome, contaSaldo, contaSenha
    print('Dados da conta:')
    print('       Nome:', contaNome)
    print('       Saldo:', contaSaldo)
    print('       Senha:', contaSenha)
    print()

def verSaldo(senha):
    global contaSaldo, contaSenha
    if senha != contaSenha:
        print('Senha incorreta!')
        return None
    
    return contaSaldo

def depositar(valorDepositado, senha):
    global contaSaldo, contaSenha

    if valorDepositado < 0:
        print('Você não pode depositar um valor negativo!')
        return None

    if senha != contaSenha:
        print('Senha incorreta!')
        return None

    contaSaldo += valorDepositado
    return contaSaldo

def sacar(valorSacado, senha):
    global contaSaldo, contaSenha

    if valorSacado < 0:
        print('Você não pode sacar um valor negativo!')
        return None

    if senha != contaSenha:
        print('Senha incorreta!')
        return None

    if valorSacado > contaSaldo:
        print('Você não pode sacar mais do que o seu saldo!')
        return None

    contaSaldo -= valorSacado
    return contaSaldo

novaConta("Joe", 100, "minhasenha")

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
        saldo = verSaldo(senha)
        if senha != contaSenha:       
            print('Senha incorreta!')
        else:            
            print('Seu saldo é:', saldo)

    elif acao == 'd':
        print('Depositar:')
        valorDepositado = input('Digite o valor que será depositado: ')
        valorDepositado = int(valorDepositado)
        senha = input('Digite sua senha: ')
        novoSaldo = depositar(valorDepositado, senha)

        if novoSaldo is not None:
            print('Seu novo saldo é:', novoSaldo)      

    elif acao == 's':  # show
        dadosConta()

    elif acao == 'q':
        break

    elif acao == 'w':
        print('Saque:')

        valorSacado = input('Digite o valor do saque: ')
        valorSacado = int(valorSacado)
        senha = input('Digite sua senha: ')
        novoSaldo = sacar(valorSacado, senha)

        if novoSaldo is not None:
            print('Seu novo saldo é:', novoSaldo)

print('Fim do programa!')