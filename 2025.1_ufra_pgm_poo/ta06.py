# ------------------------------
# Biblioteca Virtual (sem herança)
# ------------------------------

class Livro:
    def __init__(self, titulo, autor, ano, paginas):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.paginas = paginas

    def informacoes(self):
        return f'Livro: "{self.titulo}", Autor: {self.autor}, Ano: {self.ano}, Páginas: {self.paginas}'

    def __str__(self):
        return f'Livro: {self.titulo} ({self.ano})'

    def __len__(self):
        return self.paginas

    def __eq__(self, outro):
        if not isinstance(outro, Livro):
            return False
        return self.titulo == outro.titulo and self.autor == outro.autor


class Revista:
    def __init__(self, titulo, autor, ano, edicao, artigos_internos=12):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.edicao = edicao
        self.artigos_internos = artigos_internos

    def informacoes(self):
        return f'Revista: "{self.titulo}", Autor: {self.autor}, Ano: {self.ano}, Edição: {self.edicao}'

    def __str__(self):
        return f'Revista: {self.titulo} (Edição {self.edicao})'

    def __len__(self):
        return self.artigos_internos

    def __eq__(self, outro):
        if not isinstance(outro, Revista):
            return False
        return self.titulo == outro.titulo and self.autor == outro.autor


class Artigo:
    def __init__(self, titulo, autor, ano, doi):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.doi = doi

    def informacoes(self):
        return f'Artigo: "{self.titulo}", Autor: {self.autor}, Ano: {self.ano}, DOI: {self.doi}'

    def __str__(self):
        return f'Artigo: {self.titulo}'

    def __len__(self):
        return len(self.titulo)

    def __eq__(self, outro):
        if not isinstance(outro, Artigo):
            return False
        return self.titulo == outro.titulo and self.autor == outro.autor


# ------------------------------
# Demonstração do Polimorfismo
# ------------------------------

livro1 = Livro("Python Essencial", "João Silva", 2020, 350)
livro2 = Livro("Python Essencial", "João Silva", 2020, 350)
revista1 = Revista("Ciência Hoje", "Vários", 2022, 58)
artigo1 = Artigo("Machine Learning Applications", "Ana Costa", 2021, "10.1234/mlapp")

# Lista com diferentes tipos de itens (duck typing)
itens = [livro1, revista1, artigo1]

# Polimorfismo: todos respondem ao método informacoes()
for item in itens:
    print(item.informacoes())

print("\n--- Testando métodos dunder ---")
print("print(livro1) →", livro1)
print("print(revista1) →", revista1)
print("print(artigo1) →", artigo1)

print("len(livro1) →", len(livro1))
print("len(revista1) →", len(revista1))
print("len(artigo1) →", len(artigo1))

print("livro1 == livro2 →", livro1 == livro2)
print("livro1 == artigo1 →", livro1 == artigo1)  # Deve ser False
