# dominio.py
# Aqui eu defino toda a lógica de entidades da biblioteca: Itens, Usuários e Transações
# Importo a classe base EntidadeBiblioteca e Transacao (vem do nucleo.py)
from nucleo import EntidadeBiblioteca, Transacao

# =========================
# Itens (livros, revistas, dvds)
# =========================
class Item(EntidadeBiblioteca):
    def __init__(self, titulo, id_=None, status="disponivel", criado_em=None):
        # reaproveito a lógica do EntidadeBiblioteca (id, status, criado_em)
        super().__init__(id_=id_, status=status, criado_em=criado_em)
        self.__titulo = titulo   # título é obrigatório

    @property
    def titulo(self): 
        return self.__titulo

    def atualizar_status(self, novo_status): 
        # só mudo o status do item
        self.status = novo_status

    def validar(self):
        # regra básica: não pode existir item sem título
        if not self.titulo:
            raise ValueError("titulo obrigatorio")

    def para_dict(self):
        # retorno em forma de dicionário (bom pra salvar em json)
        return {
            "tipo": "Item",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "titulo": self.titulo
        }

    def mostrar_info(self): 
        # representação em string (mais legível no print)
        return f"[Item] {self.titulo}"


# ===== Subclasse Livro =====
class Livro(Item):
    def __init__(self, titulo, autor, **kw):
        super().__init__(titulo, **kw)
        self.autor = autor  # cada livro precisa de um autor

    def mostrar_info(self):
        return f"[Livro] {self.titulo} - {self.autor}"

    def para_dict(self):
        return {
            "tipo": "Livro",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "titulo": self.titulo,
            "autor": self.autor
        }


# ===== Subclasse Revista =====
class Revista(Item):
    def __init__(self, titulo, edicao, **kw):
        super().__init__(titulo, **kw)
        self.edicao = edicao  # cada revista tem uma edição

    def mostrar_info(self):
        return f"[Revista] {self.titulo} - Edicao {self.edicao}"

    def para_dict(self):
        return {
            "tipo": "Revista",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "titulo": self.titulo,
            "edicao": self.edicao
        }


# ===== Subclasse Dvd =====
class Dvd(Item):
    def __init__(self, titulo, duracao_min, **kw):
        super().__init__(titulo, **kw)
        self.duracao_min = int(duracao_min)  # guardo em inteiro

    def mostrar_info(self):
        return f"[DVD] {self.titulo} - {self.duracao_min} min"

    def para_dict(self):
        return {
            "tipo": "Dvd",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "titulo": self.titulo,
            "duracao_min": self.duracao_min
        }


# =========================
# Usuarios
# =========================
class Usuario(EntidadeBiblioteca):
    def __init__(self, nome, limite, id_=None, status="ok", criado_em=None, emprestados=0):
        # limite = quantos itens pode emprestar
        super().__init__(id_=id_, status=status, criado_em=criado_em)
        self.__nome = nome
        self.__limite = int(limite)
        self.__emprestados = int(emprestados)  # contador de quantos já pegou

    @property
    def nome(self): 
        return self.__nome

    @property
    def emprestados(self): 
        return self.__emprestados

    def pode_emprestar(self): 
        # só pode emprestar se ainda não bateu o limite
        return self.__emprestados < self.__limite

    def add_emprestado(self): 
        # incremento de item emprestado
        self.__emprestados += 1

    def rem_emprestado(self): 
        # devolução => decremento, mas nunca menor que 0
        self.__emprestados = max(0, self.__emprestados - 1)

    def mostrar_info(self): 
        return f"[Usuario] {self.nome} ({self.emprestados}/{self.__limite})"

    def atualizar_status(self, novo_status): 
        self.status = novo_status

    def validar(self):
        if not self.nome:
            raise ValueError("nome obrigatorio")

    def para_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "nome": self.nome,
            "emprestados": self.emprestados,
            "limite": self.__limite
        }


# ===== Tipos de usuário (herdam de Usuario com limite fixo) =====
class Aluno(Usuario):
    def __init__(self, nome, **kw):
        super().__init__(nome, limite=3, **kw)  # aluno pode 3


class Professor(Usuario):
    def __init__(self, nome, **kw):
        super().__init__(nome, limite=10, **kw) # professor pode 10


class Visitante(Usuario):
    def __init__(self, nome, **kw):
        super().__init__(nome, limite=1, **kw)  # visitante só 1


# =========================
# Transacoes (emprestimo e devolucao)
# =========================
class Emprestimo(Transacao):
    def __init__(self, usuario_id, item_id, **kw):
        super().__init__(**kw)
        self.usuario_id = usuario_id
        self.item_id = item_id

    def mostrar_info(self):
        return f"[Emprestimo] u={self.usuario_id} -> i={self.item_id}"

    def processar(self, usuario, item):
        # regras de negócio do empréstimo
        if item.status != "disponivel":
            raise ValueError("item indisponivel")
        if not usuario.pode_emprestar():
            raise ValueError("limite atingido")
        item.atualizar_status("emprestado")
        usuario.add_emprestado()

    def validar(self): 
        pass  # aqui poderia colocar regras extras se quisesse

    def para_dict(self):
        return {
            "tipo": "Emprestimo",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "usuario_id": self.usuario_id,
            "item_id": self.item_id
        }

    def atualizar_status(self, novo_status):
        self.status = novo_status


class Devolucao(Transacao):
    def __init__(self, usuario_id, item_id, **kw):
        super().__init__(**kw)
        self.usuario_id = usuario_id
        self.item_id = item_id

    def mostrar_info(self):
        return f"[Devolucao] u={self.usuario_id} <- i={self.item_id}"

    def processar(self, usuario, item):
        # regras da devolução: item volta a ficar disponível e usuário perde um emprestado
        item.atualizar_status("disponivel")
        usuario.rem_emprestado()

    def validar(self): 
        pass

    def para_dict(self):
        return {
            "tipo": "Devolucao",
            "id": self.id,
            "status": self.status,
            "criado_em": self.criado_em,
            "usuario_id": self.usuario_id,
            "item_id": self.item_id
        }

    def atualizar_status(self, novo_status):
        self.status = novo_status


# =========================
# Teste rapido (rodo só se chamar este arquivo direto)
# =========================
if __name__ == "__main__":
    l = Livro("Python", "Guido")
    r = Revista("Ciencia Hoje", "102")
    d = Dvd("Interstellar", 169)
    a = Aluno("Danilo")

    # prints só pra verificar se tudo ta certo
    print(l.mostrar_info())
    print(r.mostrar_info())
    print(d.mostrar_info())
    print(a.mostrar_info())
