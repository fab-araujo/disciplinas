contaNome = 'Joe'
contaSaldo = 100
contaSenha = 'minhasenha'

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
        if senha != contaSenha:       
            print('Senha incorreta!')
        else:
            print('Seu saldo é:', contaSaldo)

    elif acao == 'd':
        print('Depositar:')
        valorDepositado = input('Digite o valor que será depositado: ')
        valorDepositado = int(valorDepositado)
        senha = input('Digite sua senha: ')

        if valorDepositado < 0:
            print('Você não pode depositar um valor negativo!')

        elif senha != contaSenha:
            print('Senha incorreta!')

        else:  #OK
            contaSaldo = contaSaldo + valorDepositado
            print('Seu novo saldo é:', contaSaldo)       

    elif acao == 's':  # show
        print('Dados da conta:')
        print('       Nome', contaNome)
        print('       Balance:', contaSaldo)
        print('       Password:', contaSenha)
        print()

    elif acao == 'q':
        break

    elif acao == 'w':
        print('Saque:')

        valorSacado = input('Digite o valor do saque: ')
        valorSacado = int(valorSacado)
        senha = input('Digite sua senha: ')

        if valorSacado < 0:
            print('Você não pode sacar um valor negativo!')

        elif senha != contaSenha:
            print('Senha incorreta!')

        elif valorSacado > contaSaldo:
            print('Você não pode sacar mais do que o seu saldo!')

        else:  #OK
            contaSaldo = contaSaldo - valorSacado
            print('Seu novo saldo é:', contaSaldo)

print('Fim do programa!')