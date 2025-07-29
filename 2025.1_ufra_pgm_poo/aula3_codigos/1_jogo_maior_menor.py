import random

# Definições das cartas e naipes
nomes_cartas = ['Ás', 'Dois', 'Três', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez', 'Valete', 'Dama', 'Rei']
naipes = ['Paus', 'Ouros', 'Copas', 'Espadas']

# Criação do baralho
def criar_baralho():
    baralho = []
    for valor in range(1, 14):  # 1 para Ás, 11 para Valete, 12 para Dama, 13 para Rei
        nome = nomes_cartas[valor - 1]  # Ajuste para o índice da lista
        for naipe in naipes:
            baralho.append(
                {
                    'carta': nome, 
                    'naipe': naipe, 
                    'valor': valor
                }
            )
    return baralho

# Função principal do jogo
def jogar_maior_menor():
    baralho = criar_baralho()
    random.shuffle(baralho)
    cartas_jogo = list(baralho[0:8])  # Copia o baralho para as cartas do jogo

    pontos = 0
    carta_atual = cartas_jogo.pop(0)
    print(f"Carta inicial: {carta_atual['carta']} de {carta_atual['naipe']}")

    contador_cartas = 2
    while cartas_jogo:
        palpite = input("A próxima carta ["+str(contador_cartas)+"] é maior ou menor? (Digite maior ou menor): ").strip().lower()
        proxima_carta = cartas_jogo.pop(0)
        print(f"Próxima carta: {proxima_carta['carta']} de {proxima_carta['naipe']}")

        if proxima_carta['valor'] > carta_atual['valor']:
            resultado = 'maior'
        elif proxima_carta['valor'] < carta_atual['valor']:
            resultado = 'menor'
        else:
            resultado = 'igual'

        if resultado == palpite:
            pontos += 20
            print("Você acertou! +20 pontos.")
        elif resultado == "igual":
            pass
        else:
            pontos -= 15
            print("Você errou! -15 pontos.")

        carta_atual = proxima_carta
        contador_cartas += 1
        print(f"Pontuação atual: {pontos}\n")

    print(f"Fim do jogo! Sua pontuação final foi: {pontos}")

# Início do jogo
print("Bem-vindo ao jogo Maior ou Menor!")
print("Você terá que adivinhar se a próxima carta é maior ou menor que a atual.")
print("Se você acertar, você ganha 20 pontos! Mas se errar, perde 15 pontos.")
print("Vamos começar!\n")
jogar_maior_menor()