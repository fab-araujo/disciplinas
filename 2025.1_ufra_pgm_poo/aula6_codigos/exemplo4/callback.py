def cumprimentar(name):
    print(f"Olá, {name}!")

def processar_entrada(callback):
    name = input("Digite seu nome: ")
    callback(name)

processar_entrada("cumprimentar")