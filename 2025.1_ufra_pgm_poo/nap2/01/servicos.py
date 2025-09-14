# servicos.py
# Esse arquivo concentra as funções de serviço (operações que mexem com listas).
# Tipo um "controlador": cria, busca, processa empréstimos/devoluções e gera relatórios.

from dominio import Emprestimo, Devolucao

def achar_por_id(lista, id_):
    # função utilitária: percorro a lista e retorno o objeto com o id que bate
    for obj in lista:
        if obj.id == id_: 
            return obj
    return None   # se não achar, retorno None

# ===== CRUD básico =====
def criar_item(lista_itens, item): 
    # só adiciono o item na lista
    lista_itens.append(item)

def criar_usuario(lista_usuarios, usuario): 
    # só adiciono o usuário na lista
    lista_usuarios.append(usuario)

# ===== Processamento de Empréstimos =====
def processar_emprestimo(usuarios, itens, transacoes, usuario_id, item_id):
    # primeiro acho o usuário e o item
    u = achar_por_id(usuarios, usuario_id)
    i = achar_por_id(itens, item_id)
    if not u or not i: 
        # se algum não existe, não faço nada
        return
    # crio a transação de empréstimo
    e = Emprestimo(usuario_id, item_id)
    # aplico a regra (isso altera o status do item e soma emprestado do usuário)
    e.processar(u, i)
    # guardo a transação no histórico
    transacoes.append(e)

# ===== Processamento de Devoluções =====
def processar_devolucao(usuarios, itens, transacoes, usuario_id, item_id):
    u = achar_por_id(usuarios, usuario_id)
    i = achar_por_id(itens, item_id)
    if not u or not i: 
        return
    # crio a transação de devolução
    d = Devolucao(usuario_id, item_id)
    # aplico a regra (isso libera o item e diminui contador do usuário)
    d.processar(u, i)
    # guardo a transação no histórico
    transacoes.append(d)

# ===== Relatórios simples =====
def relatorio_disponiveis(itens):  
    # filtro só os itens que estão disponíveis
    return [i for i in itens if i.status == "disponivel"]

def relatorio_emprestados(itens): 
    # filtro só os itens que estão emprestados
    return [i for i in itens if i.status == "emprestado"]

# ===== Teste rápido =====
if __name__ == "__main__":
    print("OK: servicos.py pronto")  # se rodar direto, só mostra essa msg
