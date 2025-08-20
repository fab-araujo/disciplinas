class Livro:
    def __init__(self, titulo, autor):
        self._titulo = titulo
        self._autor = autor
        self._disponivel = True  # começa disponível

    def get_titulo(self):
        return self._titulo

    def esta_disponivel(self):
        return self._disponivel

    # Método privado para mudar disponibilidade
    def _alterar_disponibilidade(self, status: bool):
        self._disponivel = status


class Usuario:
    def __init__(self, nome, id_usuario):
        self._nome = nome
        self._id = id_usuario
        self._livros_emprestados = []

    def get_nome(self):
        return self._nome

    def listar_livros(self):
        return [livro.get_titulo() for livro in self._livros_emprestados]

    # Métodos privados para manipular livros emprestados
    def _adicionar_livro(self, livro: Livro):
        self._livros_emprestados.append(livro)

    def _remover_livro(self, livro: Livro):
        self._livros_emprestados.remove(livro)


class Biblioteca:
    def __init__(self):
        self._livros = []
        self._usuarios = []

    def cadastrar_livro(self, titulo, autor):
        self._livros.append(Livro(titulo, autor))

    def cadastrar_usuario(self, nome, id_usuario):
        self._usuarios.append(Usuario(nome, id_usuario))

    def listar_livros_disponiveis(self):
        print("\nLivros disponíveis:")
        for livro in self._livros:
            if livro.esta_disponivel():
                print(f"- {livro.get_titulo()}")

    def emprestar_livro(self, id_usuario, titulo_livro):
        usuario = self._buscar_usuario(id_usuario)
        livro = self._buscar_livro(titulo_livro)

        if usuario is None:
            print("Usuário não encontrado.")
            return
        if livro is None:
            print("Livro não encontrado.")
            return
        if not livro.esta_disponivel():
            print("Livro já emprestado.")
            return

        # Operações internas protegidas por encapsulamento
        livro._alterar_disponibilidade(False)
        usuario._adicionar_livro(livro)
        print(f"Empréstimo realizado: {usuario.get_nome()} pegou '{livro.get_titulo()}'.")

    def devolver_livro(self, id_usuario, titulo_livro):
        usuario = self._buscar_usuario(id_usuario)
        if usuario is None:
            print("Usuário não encontrado.")
            return

        # Encontrar o livro entre os emprestados
        for livro in usuario.listar_livros():
            if livro == titulo_livro:
                livro_obj = self._buscar_livro(titulo_livro)
                livro_obj._alterar_disponibilidade(True)
                usuario._remover_livro(livro_obj)
                print(f"Devolução realizada: '{titulo_livro}' devolvido por {usuario.get_nome()}.")
                return

        print("Esse usuário não possui este livro emprestado.")

    # Métodos privados para busca
    def _buscar_usuario(self, id_usuario):
        for usuario in self._usuarios:
            if usuario._id == id_usuario:  # Aqui, acesso direto só dentro da classe
                return usuario
        return None

    def _buscar_livro(self, titulo_livro):
        for livro in self._livros:
            if livro.get_titulo() == titulo_livro:
                return livro
        return None


# ======== Script de Teste ========

biblioteca = Biblioteca()

# Cadastro inicial
biblioteca.cadastrar_livro("Python Avançado", "João Silva")
biblioteca.cadastrar_livro("Inteligência Artificial", "Maria Souza")
biblioteca.cadastrar_livro("Banco de Dados Moderno", "Paulo Lima")

biblioteca.cadastrar_usuario("Carlos", 1)
biblioteca.cadastrar_usuario("Ana", 2)

biblioteca.listar_livros_disponiveis()

# Empréstimos
biblioteca.emprestar_livro(1, "Python Avançado")
biblioteca.emprestar_livro(1, "Python Avançado")  # Tentativa de repetir empréstimo

biblioteca.listar_livros_disponiveis()

# Devolução
biblioteca.devolver_livro(1, "Python Avançado")
biblioteca.listar_livros_disponiveis()

# Violação de encapsulamento (não recomendado, mas para demonstrar)
print("\nAcessando diretamente atributo privado (má prática!):")
print(biblioteca._livros[0]._disponivel)  # Isso fura o encapsulamento
