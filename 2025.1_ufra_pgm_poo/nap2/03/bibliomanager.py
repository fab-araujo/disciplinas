import pygame  # Biblioteca para criar a interface gráfica
import json  # Biblioteca para trabalhar com arquivos JSON (salvar/carregar dados)
import abc  # Biblioteca para classes abstratas (ABC)
from datetime import datetime, timedelta  # Para trabalhar com datas e horas
from typing import Dict, List, Optional  # Para tipagem de dados (melhor organização)

# Inicialização do Pygame
pygame.init()  # Inicializa todos os módulos do Pygame
pygame.font.init()  # Inicializa o módulo de fontes do Pygame

# Configurações de cores (RGB)
BRANCO, PRETO = (255, 255, 255), (0, 0, 0)  # Cores básicas
CINZA, AZUL_CLARO = (200, 200, 200), (100, 180, 255)  # Cores para elementos UI
AZUL, VERDE, VERMELHO = (0, 120, 255), (0, 200, 0), (255, 0, 0)  # Cores principais
CINZA_ESCURO, AMARELO = (100, 100, 100), (255, 255, 0)  # Cores para detalhes
VERMELHO_CLARO = (255, 100, 100)  # Vermelho mais claro para hover

# Configurações de tamanho da janela
LARGURA, ALTURA = 1024, 768  # Dimensões da janela do programa

# Configurações de fontes (tamanhos diferentes para hierarquia visual)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 14)  # Fonte pequena para detalhes
FONTE_MEDIA = pygame.font.SysFont("Arial", 18)  # Fonte média para textos normais
FONTE_TITULO = pygame.font.SysFont("Arial", 32, bold=True)  # Fonte grande para títulos

# Classe abstrata base para todas as entidades da biblioteca
class EntidadeBiblioteca(abc.ABC):
    _proximo_id = 1  # Variável de classe para con  trolar IDs únicos
    
    def __init__(self, nome: str):
        # Atributos privados (encapsulamento)
        self.__id = EntidadeBiblioteca._proximo_id  # ID único automático
        EntidadeBiblioteca._proximo_id += 1  # Incrementa para próximo ID
        self.__nome = nome  # Nome da entidade
        self.__data_criacao = datetime.now()  # Data/hora de criação
    
    # Properties para acesso controlado aos atributos privados
    @property
    def id(self) -> int: return self.__id  # Getter para ID (apenas leitura)
    
    @property
    def nome(self) -> str: return self.__nome  # Getter para nome
    
    @nome.setter
    def nome(self, valor: str): self.__nome = valor  # Setter para nome
    
    @property
    def data_criacao(self) -> datetime: return self.__data_criacao  # Getter para data
    
    # Métodos abstratos que devem ser implementados pelas subclasses
    @abc.abstractmethod
    def exibir_info(self) -> str: pass  # Retorna informações para display
    
    @abc.abstractmethod
    def atualizar_status(self, novo_status: str) -> bool: pass  # Atualiza status
    
    @abc.abstractmethod
    def validar(self) -> bool: pass  # Valida os dados da entidade
    
    @abc.abstractmethod
    def serializar(self) -> Dict: pass  # Converte para dicionário (JSON)
    
    # Método de classe para controlar IDs ao carregar dados
    @classmethod
    def definir_proximo_id(cls, proximo_id: int): cls._proximo_id = proximo_id

# Classe abstrata para itens da biblioteca (herda de EntidadeBiblioteca)
class Item(EntidadeBiblioteca, abc.ABC):
    def __init__(self, nome: str, status: str = "disponivel"):
        super().__init__(nome)  # Chama construtor da classe pai
        self.__status = status  # Status do item (disponivel, emprestado, reservado)
    
    # Property para acesso controlado ao status
    @property
    def status(self) -> str: return self.__status
    
    @status.setter
    def status(self, valor: str): self.__status = valor
    
    def atualizar_status(self, novo_status: str) -> bool:
        # Verifica se o novo status é válido antes de atualizar
        if novo_status not in ["disponivel", "emprestado", "reservado"]: return False
        self.__status = novo_status
        return True
    
    def validar(self) -> bool: return bool(self.nome)  # Validação básica
    
    def esta_disponivel(self) -> bool: return self.__status == "disponivel"  # Verifica disponibilidade

# Classe concreta para livros (herda de Item)
class Livro(Item):
    def __init__(self, titulo: str, autor: str, isbn: str, ano: int):
        super().__init__(titulo)  # Chama construtor da classe pai (Item)
        self.autor = autor  # Autor do livro
        self.isbn = isbn  # ISBN do livro
        self.ano = ano  # Ano de publicação
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações do livro
        return f"Livro: {self.nome} | Autor: {self.autor} | Ano: {self.ano} | Status: {self.status}"
    
    def validar(self) -> bool:
        # Validação específica para livros
        return super().validar() and bool(self.autor) and bool(self.isbn) and self.ano > 0
    
    def serializar(self) -> Dict:
        # Converte livro para dicionário (para salvar em JSON)
        return {
            "tipo": "Livro", "id": self.id, "titulo": self.nome, 
            "autor": self.autor, "isbn": self.isbn, "ano": self.ano, 
            "status": self.status
        }

# Classe concreta para revistas (herda de Item)
class Revista(Item):
    def __init__(self, titulo: str, edicao: str, data: str):
        super().__init__(titulo)  # Chama construtor da classe pai (Item)
        self.edicao = edicao  # Edição da revista
        self.data = data  # Data de publicação
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações da revista
        return f"Revista: {self.nome} | Edição: {self.edicao} | Data: {self.data} | Status: {self.status}"
    
    def validar(self) -> bool:
        # Validação específica para revistas
        return super().validar() and bool(self.edicao) and bool(self.data)
    
    def serializar(self) -> Dict:
        # Converte revista para dicionário (para salvar em JSON)
        return {
            "tipo": "Revista", "id": self.id, "titulo": self.nome, 
            "edicao": self.edicao, "data": self.data, "status": self.status
        }

# Classe concreta para DVDs (herda de Item)
class DVD(Item):
    def __init__(self, titulo: str, diretor: str, duracao: int):
        super().__init__(titulo)  # Chama construtor da classe pai (Item)
        self.diretor = diretor  # Diretor do DVD
        self.duracao = duracao  # Duração em minutos
    
    def exibir_info(self) -> str:
        # Converte duração para horas e minutos
        h, m = self.duracao // 60, self.duracao % 60
        # Retorna string formatada com informações do DVD
        return f"DVD: {self.nome} | Diretor: {self.diretor} | Duração: {h}h{m}min | Status: {self.status}"
    
    def validar(self) -> bool:
        # Validação específica para DVDs
        return super().validar() and bool(self.diretor) and self.duracao > 0
    
    def serializar(self) -> Dict:
        # Converte DVD para dicionário (para salvar em JSON)
        return {
            "tipo": "DVD", "id": self.id, "titulo": self.nome, 
            "diretor": self.diretor, "duracao": self.duracao, "status": self.status
        }

# Classe abstrata para usuários (herda de EntidadeBiblioteca)
class Usuario(EntidadeBiblioteca, abc.ABC):
    def __init__(self, nome: str, email: str):
        super().__init__(nome)  # Chama construtor da classe pai
        self.email = email  # Email do usuário
        self.itens_emprestados = []  # Lista de IDs dos itens emprestados
    
    def emprestar_item(self, item_id: int) -> bool:
        # Adiciona item à lista de emprestados se não estiver já emprestado
        if item_id not in self.itens_emprestados:
            self.itens_emprestados.append(item_id)
            return True
        return False
    
    def devolver_item(self, item_id: int) -> bool:
        # Remove item da lista de emprestados se estiver emprestado
        if item_id in self.itens_emprestados:
            self.itens_emprestados.remove(item_id)
            return True
        return False
    
    @abc.abstractmethod
    def pode_emprestar(self, quantidade_itens: int = 1) -> bool: pass  # Método abstrato
    
    def atualizar_status(self, novo_status: str) -> bool: return True  # Para usuários, status não é aplicável
    
    def validar(self) -> bool: return bool(self.nome) and "@" in self.email  # Validação básica
    
    def serializar(self) -> Dict:
        # Converte usuário para dicionário (para salvar em JSON)
        return {
            "tipo": self.__class__.__name__, "id": self.id, "nome": self.nome,
            "email": self.email, "itens_emprestados": self.itens_emprestados
        }

# Classe concreta para estudantes (herda de Usuario)
class Estudante(Usuario):
    MAXIMO_ITENS = 3  # Limite máximo de itens que um estudante pode emprestar
    
    def __init__(self, nome: str, email: str, id_estudante: str):
        super().__init__(nome, email)  # Chama construtor da classe pai (Usuario)
        self.id_estudante = id_estudante  # ID específico do estudante
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações do estudante
        return f"Estudante: {self.nome} | ID: {self.id_estudante} | Itens: {len(self.itens_emprestados)}/{self.MAXIMO_ITENS}"
    
    def pode_emprestar(self, quantidade_itens: int = 1) -> bool:
        # Verifica se o estudante pode emprestar mais itens
        return len(self.itens_emprestados) + quantidade_itens <= self.MAXIMO_ITENS
    
    def validar(self) -> bool:
        # Validação específica para estudantes
        return super().validar() and bool(self.id_estudante)
    
    def serializar(self) -> Dict:
        # Converte estudante para dicionário (para salvar em JSON)
        dados = super().serializar()  # Chama serialização da classe pai
        dados["id_estudante"] = self.id_estudante  # Adiciona campo específico
        return dados

# Classe concreta para professores (herda de Usuario)
class Professor(Usuario):
    def __init__(self, nome: str, email: str, departamento: str):
        super().__init__(nome, email)  # Chama construtor da classe pai (Usuario)
        self.departamento = departamento  # Departamento do professor
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações do professor
        return f"Professor: {self.nome} | Departamento: {self.departamento} | Itens: {len(self.itens_emprestados)}"
    
    def pode_emprestar(self, quantidade_itens: int = 1) -> bool: 
        return True  # Professores não têm limite de empréstimos
    
    def validar(self) -> bool:
        # Validação específica para professores
        return super().validar() and bool(self.departamento)
    
    def serializar(self) -> Dict:
        # Converte professor para dicionário (para salvar em JSON)
        dados = super().serializar()  # Chama serialização da classe pai
        dados["departamento"] = self.departamento  # Adiciona campo específico
        return dados

# Classe concreta para visitantes (herda de Usuario)
class Visitante(Usuario):
    MAXIMO_ITENS = 1  # Limite máximo de itens que um visitante pode emprestar
    
    def __init__(self, nome: str, email: str, telefone: str):
        super().__init__(nome, email)  # Chama construtor da classe pai (Usuario)
        self.telefone = telefone  # Telefone do visitante
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações do visitante
        return f"Visitante: {self.nome} | Telefone: {self.telefone} | Itens: {len(self.itens_emprestados)}/{self.MAXIMO_ITENS}"
    
    def pode_emprestar(self, quantidade_itens: int = 1) -> bool:
        # Verifica se o visitante pode emprestar mais itens
        return len(self.itens_emprestados) + quantidade_itens <= self.MAXIMO_ITENS
    
    def validar(self) -> bool:
        # Validação específica para visitantes
        return super().validar() and bool(self.telefone)
    
    def serializar(self) -> Dict:
        # Converte visitante para dicionário (para salvar em JSON)
        dados = super().serializar()  # Chama serialização da classe pai
        dados["telefone"] = self.telefone  # Adiciona campo específico
        return dados

# Classe abstrata para transações (herda de EntidadeBiblioteca)
class Transacao(EntidadeBiblioteca, abc.ABC):
    def __init__(self, id_usuario: int, id_item: int):
        # Cria nome único para a transação baseado nos IDs
        super().__init__(f"Transacao_{id_usuario}_{id_item}")
        self.id_usuario = id_usuario  # ID do usuário envolvido
        self.id_item = id_item  # ID do item envolvido
        self.data_transacao = datetime.now()  # Data/hora da transação
    
    @abc.abstractmethod
    def processar(self, usuario: Usuario, item: Item) -> bool: pass  # Método abstrato
    
    def atualizar_status(self, novo_status: str) -> bool: return True  # Para transações, status não é aplicável
    
    def validar(self) -> bool: return self.id_usuario > 0 and self.id_item > 0  # Validação básica
    
    def serializar(self) -> Dict:
        # Converte transação para dicionário (para salvar em JSON)
        return {
            "tipo": self.__class__.__name__, "id": self.id, "id_usuario": self.id_usuario,
            "id_item": self.id_item, "data": self.data_transacao.isoformat()
        }

# Classe concreta para empréstimos (herda de Transacao)
class Emprestimo(Transacao):
    def __init__(self, id_usuario: int, id_item: int):
        super().__init__(id_usuario, id_item)  # Chama construtor da classe pai
        self.data_vencimento = datetime.now() + timedelta(days=14)  # Data de vencimento (14 dias)
    
    def exibir_info(self) -> str:
        # Retorna string formatada com informações do empréstimo
        return f"Empréstimo: Usuário #{self.id_usuario} → Item #{self.id_item} | Vencimento: {self.data_vencimento.strftime('%d/%m/%Y')}"
    
    def processar(self, usuario: Usuario, item: Item) -> bool:
        # Processa o empréstimo se o item estiver disponível e o usuário puder emprestar
        if not item.esta_disponivel() or not usuario.pode_emprestar(): return False
        return usuario.emprestar_item(item.id) and item.atualizar_status("emprestado")
    
    def serializar(self) -> Dict:
        # Converte empréstimo para dicionário (para salvar em JSON)
        dados = super().serializar()  # Chama serialização da classe pai
        dados["data_vencimento"] = self.data_vencimento.isoformat()  # Adiciona campo específico
        return dados

# Classe concreta para devoluções (herda de Transacao)
class Devolucao(Transacao):
    def exibir_info(self) -> str:
        # Retorna string formatada com informações da devolução
        return f"Devolução: Usuário #{self.id_usuario} → Item #{self.id_item}"
    
    def processar(self, usuario: Usuario, item: Item) -> bool:
        # Processa a devolução se o item estiver emprestado para o usuário
        if item.status != "emprestado" or self.id_item not in usuario.itens_emprestados: return False
        return usuario.devolver_item(item.id) and item.atualizar_status("disponivel")

# Classe principal que gerencia toda a biblioteca
class GerenciadorBiblioteca:
    def __init__(self):
        # Dicionários para armazenar todas as entidades
        self.itens: Dict[int, Item] = {}  # {id: Item}
        self.usuarios: Dict[int, Usuario] = {}  # {id: Usuario}
        self.transacoes: Dict[int, Transacao] = {}  # {id: Transacao}
    
    def adicionar_item(self, item: Item) -> bool:
        # Adiciona item se for válido e não existir outro com mesmo ID
        if item.validar() and item.id not in self.itens:
            self.itens[item.id] = item
            return True
        return False
    
    def remover_item(self, id_item: int) -> bool:
        # Remove item se existir e estiver disponível
        if id_item in self.itens and self.itens[id_item].status == "disponivel":
            del self.itens[id_item]
            return True
        return False
    
    def obter_item(self, id_item: int) -> Optional[Item]:
        # Retorna item pelo ID ou None se não existir
        return self.itens.get(id_item)
    
    def buscar_item_por_nome(self, nome: str) -> Optional[Item]:
        # Busca item pelo nome (case insensitive)
        for item in self.itens.values():
            if item.nome.lower() == nome.lower():
                return item
        return None
    
    def adicionar_usuario(self, usuario: Usuario) -> bool:
        # Adiciona usuário se for válido e não existir outro com mesmo ID
        if usuario.validar() and usuario.id not in self.usuarios:
            self.usuarios[usuario.id] = usuario
            return True
        return False
    
    def remover_usuario(self, id_usuario: int) -> bool:
        # Remove usuário se existir e não tiver itens emprestados
        if id_usuario in self.usuarios and not self.usuarios[id_usuario].itens_emprestados:
            del self.usuarios[id_usuario]
            return True
        return False
    
    def obter_usuario(self, id_usuario: int) -> Optional[Usuario]:
        # Retorna usuário pelo ID ou None se não existir
        return self.usuarios.get(id_usuario)
    
    def buscar_usuario_por_nome(self, nome: str) -> Optional[Usuario]:
        # Busca usuário pelo nome (case insensitive)
        for usuario in self.usuarios.values():
            if usuario.nome.lower() == nome.lower():
                return usuario
        return None
    
    def processar_transacao(self, transacao: Transacao) -> bool:
        # Processa transação se todos os dados forem válidos
        usuario = self.obter_usuario(transacao.id_usuario)
        item = self.obter_item(transacao.id_item)
        
        if not usuario or not item or not transacao.validar(): return False
        
        if transacao.processar(usuario, item):
            self.transacoes[transacao.id] = transacao
            return True
        return False
    
    def obter_itens_disponiveis(self) -> List[Item]:
        # Retorna lista de itens disponíveis para empréstimo
        return [item for item in self.itens.values() if item.esta_disponivel()]
    
    def obter_itens_emprestados(self) -> List[Item]:
        # Retorna lista de itens emprestados
        return [item for item in self.itens.values() if item.status == "emprestado"]
    
    def salvar_dados(self, nome_arquivo: str = "dados_biblioteca.json") -> bool:
        try:
            # Prepara dados para serialização
            dados = {
                "proximo_id": EntidadeBiblioteca._proximo_id,
                "itens": [item.serializar() for item in self.itens.values()],
                "usuarios": [usuario.serializar() for usuario in self.usuarios.values()],
                "transacoes": [t.serializar() for t in self.transacoes.values()]
            }
            # Salva dados em arquivo JSON
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    def carregar_dados(self, nome_arquivo: str = "dados_biblioteca.json") -> bool:
        try:
            # Carrega dados do arquivo JSON
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Configura próximo ID
            EntidadeBiblioteca.definir_proximo_id(dados.get("proximo_id", 1))
            # Limpa dados atuais
            self.itens.clear(); self.usuarios.clear(); self.transacoes.clear()
            
            # Carrega itens
            for dados_item in dados.get("itens", []):
                if dados_item["tipo"] == "Livro":
                    item = Livro(dados_item["titulo"], dados_item["autor"], dados_item["isbn"], dados_item["ano"])
                elif dados_item["tipo"] == "Revista":
                    item = Revista(dados_item["titulo"], dados_item["edicao"], dados_item["data"])
                elif dados_item["tipo"] == "DVD":
                    item = DVD(dados_item["titulo"], dados_item["diretor"], dados_item["duracao"])
                else: continue
                
                # Define ID manualmente (acesso direto ao atributo privado)
                item._EntidadeBiblioteca__id = dados_item["id"]
                item.status = dados_item.get("status", "disponivel")
                self.itens[item.id] = item
            
            # Carrega usuários
            for dados_usuario in dados.get("usuarios", []):
                if dados_usuario["tipo"] == "Estudante":
                    usuario = Estudante(dados_usuario["nome"], dados_usuario["email"], dados_usuario["id_estudante"])
                elif dados_usuario["tipo"] == "Professor":
                    usuario = Professor(dados_usuario["nome"], dados_usuario["email"], dados_usuario["departamento"])
                elif dados_usuario["tipo"] == "Visitante":
                    usuario = Visitante(dados_usuario["nome"], dados_usuario["email"], dados_usuario["telefone"])
                else: continue
                
                # Define ID manualmente (acesso direto ao atributo privado)
                usuario._EntidadeBiblioteca__id = dados_usuario["id"]
                # Restaura itens emprestados
                for id_item in dados_usuario.get("itens_emprestados", []): 
                    usuario.emprestar_item(id_item)
                self.usuarios[usuario.id] = usuario
            
            # Carrega transações
            for dados_transacao in dados.get("transacoes", []):
                if dados_transacao["tipo"] == "Emprestimo":
                    transacao = Emprestimo(dados_transacao["id_usuario"], dados_transacao["id_item"])
                    transacao._EntidadeBiblioteca__id = dados_transacao["id"]
                    transacao.data_transacao = datetime.fromisoformat(dados_transacao["data"])
                    transacao.data_vencimento = datetime.fromisoformat(dados_transacao["data_vencimento"])
                elif dados_transacao["tipo"] == "Devolucao":
                    transacao = Devolucao(dados_transacao["id_usuario"], dados_transacao["id_item"])
                    transacao._EntidadeBiblioteca__id = dados_transacao["id"]
                    transacao.data_transacao = datetime.fromisoformat(dados_transacao["data"])
                else: continue
                
                self.transacoes[transacao.id] = transacao
            
            return True
        except:
            return False

# Classe principal da aplicação com interface gráfica
class AppBiblioManager:
    def __init__(self):
        # Configuração da janela do Pygame
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("BiblioManager - Sistema de Biblioteca")
        self.relogio = pygame.time.Clock()  # Para controlar FPS
        self.executando = True  # Controla loop principal
        
        # Instancia o gerenciador da biblioteca
        self.biblioteca = GerenciadorBiblioteca()
        self.tela_atual = "menu_principal"  # Estado inicial
        
        # Dicionários para controle de interface
        self.campos_entrada = {}  # Armazena retângulos dos campos {nome: rect}
        self.valores_entrada = {}  # Armazena valores dos campos {nome: valor}
        self.campo_ativo = None  # Campo atualmente selecionado
        
        # Controle de mensagens
        self.mensagem = ""  # Mensagem atual
        self.cor_mensagem = PRETO  # Cor da mensagem
        
        # Carrega dados salvos e cria usuários exemplo
        self.biblioteca.carregar_dados()
        self.criar_usuarios_exemplo()
        
        # Define botões do menu principal
        self.botoes_menu = [
            {"retangulo": pygame.Rect(362, 200, 300, 60), "texto": "Gerenciar Itens", "acao": "gerenciar_itens"},
            {"retangulo": pygame.Rect(362, 280, 300, 60), "texto": "Gerenciar Usuários", "acao": "gerenciar_usuarios"},
            {"retangulo": pygame.Rect(362, 360, 300, 60), "texto": "Realizar Empréstimo", "acao": "emprestar_item"},
            {"retangulo": pygame.Rect(362, 440, 300, 60), "texto": "Realizar Devolução", "acao": "devolver_item"},
            {"retangulo": pygame.Rect(362, 520, 300, 60), "texto": "Sair", "acao": "sair"}
        ]
        
        # Define botões do menu de gerenciamento de itens
        self.botoes_itens = [
            {"retangulo": pygame.Rect(362, 200, 300, 60), "texto": "Adicionar Livro", "acao": "adicionar_livro"},
            {"retangulo": pygame.Rect(362, 280, 300, 60), "texto": "Adicionar Revista", "acao": "adicionar_revista"},
            {"retangulo": pygame.Rect(362, 360, 300, 60), "texto": "Adicionar DVD", "acao": "adicionar_dvd"},
            {"retangulo": pygame.Rect(362, 440, 300, 60), "texto": "Visualizar Itens", "acao": "visualizar_itens"},
            {"retangulo": pygame.Rect(362, 520, 300, 60), "texto": "Voltar", "acao": "menu_principal"}
        ]
        
        # Define botões do menu de gerenciamento de usuários
        self.botoes_usuarios = [
            {"retangulo": pygame.Rect(362, 200, 300, 60), "texto": "Adicionar Estudante", "acao": "adicionar_estudante"},
            {"retangulo": pygame.Rect(362, 280, 300, 60), "texto": "Adicionar Professor", "acao": "adicionar_professor"},
            {"retangulo": pygame.Rect(362, 360, 300, 60), "texto": "Adicionar Visitante", "acao": "adicionar_visitante"},
            {"retangulo": pygame.Rect(362, 440, 300, 60), "texto": "Visualizar Usuários", "acao": "visualizar_usuarios"},
            {"retangulo": pygame.Rect(362, 520, 300, 60), "texto": "Voltar", "acao": "menu_principal"}
        ]
        
        self.botoes_formulario = [
            {"retangulo": pygame.Rect(562, 650, 150, 50), "texto": "Confirmar", "acao": "confirmar_formulario"},
            {"retangulo": pygame.Rect(312, 650, 150, 50), "texto": "Cancelar", "acao": "cancelar_formulario"}
        ]
        
        # Botão de voltar para telas de lista
        self.botao_voltar = {"retangulo": pygame.Rect(362, 650, 300, 60), "texto": "Voltar", "acao": "menu_principal"}
    
    def criar_usuarios_exemplo(self):
        # Criar 10 usuários de exemplo se não existirem
        if len(self.biblioteca.usuarios) < 10:
            usuarios_exemplo = [
                ("João Silva", "joao@email.com", "EST123", Estudante),
                ("Maria Santos", "maria@email.com", "PROF456", Professor),
                ("Carlos Oliveira", "carlos@email.com", "VIS789", Visitante),
                ("Ana Costa", "ana@email.com", "EST101", Estudante),
                ("Pedro Alves", "pedro@email.com", "PROF202", Professor),
                ("Laura Mendes", "laura@email.com", "VIS303", Visitante),
                ("Paulo Rodrigues", "paulo@email.com", "EST404", Estudante),
                ("Fernanda Lima", "fernanda@email.com", "PROF505", Professor),
                ("Ricardo Souza", "ricardo@email.com", "VIS606", Visitante),
                ("Juliana Pereira", "juliana@email.com", "EST707", Estudante)
            ]
            
            for i, (nome, email, id, tipo) in enumerate(usuarios_exemplo):
                if tipo == Estudante:
                    usuario = tipo(nome, email, id)
                elif tipo == Professor:
                    usuario = tipo(nome, email, f"Departamento {i+1}")
                else:  # Visitante
                    usuario = tipo(nome, email, f"(11) 9{i:04d}-{i:04d}")
                
                self.biblioteca.adicionar_usuario(usuario)
    
    def executar(self):
        while self.executando:
            self.processar_eventos()
            self.renderizar()
            self.relogio.tick(60)
        self.biblioteca.salvar_dados()
        pygame.quit()
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                self.executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN: 
                self.processar_clique_mouse()
            elif evento.type == pygame.KEYDOWN and self.campo_ativo: 
                self.processar_tecla(evento)
    
    def processar_clique_mouse(self):
        pos_mouse = pygame.mouse.get_pos()
        
        if self.tela_atual == "menu_principal":
            for botao in self.botoes_menu:
                if botao["retangulo"].collidepoint(pos_mouse): 
                    self.executar_acao(botao["acao"])
        
        elif self.tela_atual == "gerenciar_itens":
            for botao in self.botoes_itens:
                if botao["retangulo"].collidepoint(pos_mouse): 
                    self.executar_acao(botao["acao"])
        
        elif self.tela_atual == "gerenciar_usuarios":
            for botao in self.botoes_usuarios:
                if botao["retangulo"].collidepoint(pos_mouse): 
                    self.executar_acao(botao["acao"])
        
        elif self.tela_atual in ["adicionar_livro", "adicionar_revista", "adicionar_dvd", "adicionar_estudante", "adicionar_professor", "adicionar_visitante", "emprestar_item", "devolver_item"]:
            # Verificar cliques nos campos de entrada
            for nome_campo, retangulo_campo in self.campos_entrada.items():
                if retangulo_campo.collidepoint(pos_mouse): 
                    self.campo_ativo = nome_campo
                    break
            else:
                self.campo_ativo = None
            
            # Verificar cliques nos botões do formulário
            for botao in self.botoes_formulario:
                if botao["retangulo"].collidepoint(pos_mouse): 
                    self.executar_acao(botao["acao"])
        
        # Verificar clique no botão voltar nas telas de lista
        elif self.tela_atual in ["visualizar_itens", "visualizar_usuarios"]:
            if self.botao_voltar["retangulo"].collidepoint(pos_mouse):
                self.executar_acao(self.botao_voltar["acao"])
    
    def processar_tecla(self, evento):
        if self.campo_ativo:
            if evento.key == pygame.K_BACKSPACE:
                self.valores_entrada[self.campo_ativo] = self.valores_entrada[self.campo_ativo][:-1]
            elif evento.key == pygame.K_RETURN:
                self.campo_ativo = None
            else:
                # Adicionar caractere ao campo ativo (limitar a 30 caracteres)
                if len(self.valores_entrada[self.campo_ativo]) < 30:
                    self.valores_entrada[self.campo_ativo] += evento.unicode
    
    def executar_acao(self, acao):
        if acao == "sair": 
            self.executando = False
        elif acao == "menu_principal": 
            self.tela_atual = "menu_principal"
            self.campos_entrada.clear()
            self.valores_entrada.clear()
            self.campo_ativo = None
            self.mensagem = ""
        
        elif acao == "gerenciar_itens": 
            self.tela_atual = "gerenciar_itens"
        elif acao == "gerenciar_usuarios": 
            self.tela_atual = "gerenciar_usuarios"
        
        elif acao == "adicionar_livro":
            self.tela_atual = "adicionar_livro"
            self.valores_entrada = {"titulo": "", "autor": "", "isbn": "", "ano": ""}
        
        elif acao == "adicionar_revista":
            self.tela_atual = "adicionar_revista"
            self.valores_entrada = {"titulo": "", "edicao": "", "data": ""}
        
        elif acao == "adicionar_dvd":
            self.tela_atual = "adicionar_dvd"
            self.valores_entrada = {"titulo": "", "diretor": "", "duracao": ""}
        
        elif acao == "visualizar_itens": 
            self.tela_atual = "visualizar_itens"
        
        elif acao == "adicionar_estudante":
            self.tela_atual = "adicionar_estudante"
            self.valores_entrada = {"nome": "", "email": "", "id_estudante": ""}
        
        elif acao == "adicionar_professor":
            self.tela_atual = "adicionar_professor"
            self.valores_entrada = {"nome": "", "email": "", "departamento": ""}
        
        elif acao == "adicionar_visitante":
            self.tela_atual = "adicionar_visitante"
            self.valores_entrada = {"nome": "", "email": "", "telefone": ""}
        
        elif acao == "visualizar_usuarios": 
            self.tela_atual = "visualizar_usuarios"
        
        elif acao == "emprestar_item":
            self.tela_atual = "emprestar_item"
            self.valores_entrada = {"nome_usuario": "", "nome_item": ""}
        
        elif acao == "devolver_item":
            self.tela_atual = "devolver_item"
            self.valores_entrada = {"nome_usuario": "", "nome_item": ""}
        
        elif acao == "confirmar_formulario": 
            self.processar_formulario()
        elif acao == "cancelar_formulario": 
            self.tela_atual = "menu_principal"
            self.campos_entrada.clear()
            self.valores_entrada.clear()
            self.campo_ativo = None
            self.mensagem = ""
    
    def processar_formulario(self):
        try:
            if self.tela_atual == "adicionar_livro":
                livro = Livro(
                    self.valores_entrada["titulo"],
                    self.valores_entrada["autor"],
                    self.valores_entrada["isbn"],
                    int(self.valores_entrada["ano"])
                )
                if self.biblioteca.adicionar_item(livro): 
                    self.mensagem = "Livro adicionado com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "adicionar_revista":
                revista = Revista(
                    self.valores_entrada["titulo"],
                    self.valores_entrada["edicao"],
                    self.valores_entrada["data"]
                )
                if self.biblioteca.adicionar_item(revista): 
                    self.mensagem = "Revista adicionada com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "adicionar_dvd":
                dvd = DVD(
                    self.valores_entrada["titulo"],
                    self.valores_entrada["diretor"],
                    int(self.valores_entrada["duracao"])
                )
                if self.biblioteca.adicionar_item(dvd): 
                    self.mensagem = "DVD adicionado com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "adicionar_estudante":
                estudante = Estudante(
                    self.valores_entrada["nome"],
                    self.valores_entrada["email"],
                    self.valores_entrada["id_estudante"]
                )
                if self.biblioteca.adicionar_usuario(estudante): 
                    self.mensagem = "Estudante adicionado com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "adicionar_professor":
                professor = Professor(
                    self.valores_entrada["nome"],
                    self.valores_entrada["email"],
                    self.valores_entrada["departamento"]
                )
                if self.biblioteca.adicionar_usuario(professor): 
                    self.mensagem = "Professor adicionado com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "adicionar_visitante":
                visitante = Visitante(
                    self.valores_entrada["nome"],
                    self.valores_entrada["email"],
                    self.valores_entrada["telefone"]
                )
                if self.biblioteca.adicionar_usuario(visitante): 
                    self.mensagem = "Visitante adicionado com sucesso!"
                    self.cor_mensagem = VERDE
                    self.tela_atual = "menu_principal"
            
            elif self.tela_atual == "emprestar_item":
                # Buscar usuário e item por nome
                usuario_encontrado = None
                item_encontrado = None
                
                for usuario in self.biblioteca.usuarios.values():
                    if usuario.nome.lower() == self.valores_entrada["nome_usuario"].lower():
                        usuario_encontrado = usuario
                        break
                
                item_encontrado = self.biblioteca.buscar_item_por_nome(self.valores_entrada["nome_item"])
                
                if usuario_encontrado and item_encontrado:
                    if item_encontrado.esta_disponivel():
                        emprestimo = Emprestimo(usuario_encontrado.id, item_encontrado.id)
                        if self.biblioteca.processar_transacao(emprestimo):
                            self.mensagem = f"Empréstimo realizado com sucesso para {usuario_encontrado.nome}!"
                            self.cor_mensagem = VERDE
                            self.tela_atual = "menu_principal"
                        else:
                            self.mensagem = "Erro ao realizar empréstimo. Verifique se o usuário pode emprestar mais itens."
                            self.cor_mensagem = VERMELHO
                    else:
                        self.mensagem = "Item não está disponível para empréstimo!"
                        self.cor_mensagem = VERMELHO
                else:
                    if not usuario_encontrado:
                        self.mensagem = "Usuário não encontrado!"
                        self.cor_mensagem = VERMELHO
                    else:
                        self.mensagem = "Item não encontrado!"
                        self.cor_mensagem = VERMELHO
            
            elif self.tela_atual == "devolver_item":
                # Buscar usuário e item por nome
                usuario_encontrado = None
                item_encontrado = None
                
                for usuario in self.biblioteca.usuarios.values():
                    if usuario.nome.lower() == self.valores_entrada["nome_usuario"].lower():
                        usuario_encontrado = usuario
                        break
                
                item_encontrado = self.biblioteca.buscar_item_por_nome(self.valores_entrada["nome_item"])
                
                if usuario_encontrado and item_encontrado:
                    if item_encontrado.status == "emprestado" and item_encontrado.id in usuario_encontrado.itens_emprestados:
                        devolucao = Devolucao(usuario_encontrado.id, item_encontrado.id)
                        if self.biblioteca.processar_transacao(devolucao):
                            self.mensagem = f"Devolução realizada com sucesso por {usuario_encontrado.nome}!"
                            self.cor_mensagem = VERDE
                            self.tela_atual = "menu_principal"
                        else:
                            self.mensagem = "Erro ao realizar devolução."
                            self.cor_mensagem = VERMELHO
                    else:
                        self.mensagem = "Este item não foi emprestado para este usuário!"
                        self.cor_mensagem = VERMELHO
                else:
                    if not usuario_encontrado:
                        self.mensagem = "Usuário não encontrado!"
                        self.cor_mensagem = VERMELHO
                    else:
                        self.mensagem = "Item não encontrado!"
                        self.cor_mensagem = VERMELHO
            
            self.valores_entrada.clear()
        except Exception as e:
            self.mensagem = f"Erro: {str(e)}"
            self.cor_mensagem = VERMELHO
    
    def renderizar(self):
        self.tela.fill(BRANCO)
        
        if self.tela_atual == "menu_principal": 
            self.renderizar_menu_principal()
        elif self.tela_atual == "gerenciar_itens": 
            self.renderizar_menu("Gerenciar Itens", self.botoes_itens)
        elif self.tela_atual == "gerenciar_usuarios": 
            self.renderizar_menu("Gerenciar Usuários", self.botoes_usuarios)
        elif self.tela_atual in ["adicionar_livro", "adicionar_revista", "adicionar_dvd", "adicionar_estudante", "adicionar_professor", "adicionar_visitante", "emprestar_item", "devolver_item"]: 
            self.renderizar_formulario()
        elif self.tela_atual == "visualizar_itens": 
            self.renderizar_lista("Itens da Biblioteca", [item.exibir_info() for item in self.biblioteca.itens.values()])
        elif self.tela_atual == "visualizar_usuarios": 
            self.renderizar_lista("Usuários da Biblioteca", [usuario.exibir_info() for usuario in self.biblioteca.usuarios.values()])
        
        # Renderizar mensagem se existir
        if self.mensagem:
            texto_mensagem = FONTE_MEDIA.render(self.mensagem, True, self.cor_mensagem)
            self.tela.blit(texto_mensagem, (LARGURA // 2 - texto_mensagem.get_width() // 2, 20))
        
        pygame.display.flip()
    
    def renderizar_menu_principal(self):
        texto_titulo = FONTE_TITULO.render("BiblioManager", True, AZUL)
        self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 80))
        
        for botao in self.botoes_menu:
            # Usar cor vermelha para o botão "Sair"
            if botao["texto"] == "Sair":
                cor = VERMELHO_CLARO if botao["retangulo"].collidepoint(pygame.mouse.get_pos()) else VERMELHO
            else:
                cor = AZUL_CLARO if botao["retangulo"].collidepoint(pygame.mouse.get_pos()) else AZUL
                
            pygame.draw.rect(self.tela, cor, botao["retangulo"], border_radius=10)
            pygame.draw.rect(self.tela, CINZA_ESCURO, botao["retangulo"], 2, border_radius=10)
            
            texto = FONTE_MEDIA.render(botao["texto"], True, BRANCO)
            self.tela.blit(texto, (botao["retangulo"].centerx - texto.get_width() // 2, botao["retangulo"].centery - texto.get_height() // 2))
    
    def renderizar_menu(self, titulo, botoes):
        texto_titulo = FONTE_TITULO.render(titulo, True, AZUL)
        self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 80))
        
        for botao in botoes:
            cor = AZUL_CLARO if botao["retangulo"].collidepoint(pygame.mouse.get_pos()) else AZUL
            pygame.draw.rect(self.tela, cor, botao["retangulo"], border_radius=10)
            pygame.draw.rect(self.tela, CINZA_ESCURO, botao["retangulo"], 2, border_radius=10)
            
            texto = FONTE_MEDIA.render(botao["texto"], True, BRANCO)
            self.tela.blit(texto, (botao["retangulo"].centerx - texto.get_width() // 2, botao["retangulo"].centery - texto.get_height() // 2))
    
    def renderizar_formulario(self):
        titulo = self.tela_atual.replace("_", " ").title()
        texto_titulo = FONTE_TITULO.render(titulo, True, AZUL)
        self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 80))
        
        y_offset = 150
        self.campos_entrada = {}  # Resetar os campos de entrada
        
        for nome_campo in self.valores_entrada.keys():
            rotulo = FONTE_MEDIA.render(nome_campo.title() + ":", True, PRETO)
            self.tela.blit(rotulo, (200, y_offset))
            
            retangulo_campo = pygame.Rect(400, y_offset, 400, 30)
            self.campos_entrada[nome_campo] = retangulo_campo
            
            cor_borda = AZUL if self.campo_ativo == nome_campo else CINZA_ESCURO
            pygame.draw.rect(self.tela, BRANCO, retangulo_campo)
            pygame.draw.rect(self.tela, cor_borda, retangulo_campo, 2)
            
            texto_valor = FONTE_MEDIA.render(self.valores_entrada[nome_campo], True, PRETO)
            self.tela.blit(texto_valor, (retangulo_campo.x + 5, retangulo_campo.y + 5))
            
            y_offset += 50
        
        for botao in self.botoes_formulario:
            cor = AZUL_CLARO if botao["retangulo"].collidepoint(pygame.mouse.get_pos()) else AZUL
            pygame.draw.rect(self.tela, cor, botao["retangulo"], border_radius=10)
            pygame.draw.rect(self.tela, CINZA_ESCURO, botao["retangulo"], 2, border_radius=10)
            
            texto = FONTE_MEDIA.render(botao["texto"], True, BRANCO)
            self.tela.blit(texto, (botao["retangulo"].centerx - texto.get_width() // 2, botao["retangulo"].centery - texto.get_height() // 2))
    
    def renderizar_lista(self, titulo, itens):
        texto_titulo = FONTE_TITULO.render(titulo, True, AZUL)
        self.tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 50))
        
        y_offset = 100
        for item in itens:
            texto_item = FONTE_PEQUENA.render(item, True, PRETO)
            self.tela.blit(texto_item, (50, y_offset))
            y_offset += 30
        
        # Renderizar botão voltar
        cor = AZUL_CLARO if self.botao_voltar["retangulo"].collidepoint(pygame.mouse.get_pos()) else AZUL
        pygame.draw.rect(self.tela, cor, self.botao_voltar["retangulo"], border_radius=10)
        pygame.draw.rect(self.tela, CINZA_ESCURO, self.botao_voltar["retangulo"], 2, border_radius=10)
        
        texto = FONTE_MEDIA.render(self.botao_voltar["texto"], True, BRANCO)
        self.tela.blit(texto, (self.botao_voltar["retangulo"].centerx - texto.get_width() // 2, self.botao_voltar["retangulo"].centery - texto.get_height() // 2))

# Executar aplicação
if __name__ == "__main__":
    app = AppBiblioManager()
    app.executar()