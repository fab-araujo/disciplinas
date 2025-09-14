# nucleo.py
# Esse arquivo é a base de tudo: define classes abstratas que os outros arquivos vão herdar.
# Aqui eu crio a EntidadeBiblioteca (qualquer coisa que tem id, status e data)
# e a Transacao (emprestimos/devoluções que precisam de processar).

from abc import ABC, abstractmethod   # pra fazer classes abstratas
from datetime import datetime         # pra carimbar data/hora de criação
import uuid                           # pra gerar ids únicos (tipo hash)

class EntidadeBiblioteca(ABC):
    def __init__(self, id_=None, status="ok", criado_em=None):
        # id: se não passar, eu crio um uuid automático
        self.__id = id_ or str(uuid.uuid4())
        # status: por padrão "ok" (mas quem herdar pode mudar isso)
        self.__status = status
        # criado_em: salvo o timestamp no formato ISO, se não passar eu gero agora
        self.__criado_em = criado_em or datetime.utcnow().isoformat()

    # ===== Propriedades básicas =====
    @property
    def id(self): 
        return self.__id  # id é só leitura

    @property
    def status(self): 
        return self.__status
    @status.setter
    def status(self, novo_status):
        # só aceito status do tipo string (pra não quebrar nada)
        if not isinstance(novo_status, str):
            raise ValueError("status deve ser string")
        self.__status = novo_status

    @property
    def criado_em(self): 
        return self.__criado_em  # carimbo de criação (string ISO)

    # ===== Métodos abstratos =====
    # quem herdar dessa classe é obrigado a implementar todos esses
    @abstractmethod
    def mostrar_info(self): 
        ...  # retorna string bonitinha com dados

    @abstractmethod
    def atualizar_status(self, novo_status): 
        ...  # muda status de forma específica da classe

    @abstractmethod
    def validar(self): 
        ...  # checagem se dados obrigatórios estão presentes

    @abstractmethod
    def para_dict(self): 
        ...  # gera dicionário (facil de salvar/exportar)


class Transacao(EntidadeBiblioteca, ABC):
    # classe base pra operações como empréstimo e devolução
    @abstractmethod
    def processar(self, usuario, item): 
        ...  # cada transação tem que definir como processar


# ===== Teste rápido =====
if __name__ == "__main__":
    print("OK: nucleo.py pronto")  # só pra eu saber que roda de boa
