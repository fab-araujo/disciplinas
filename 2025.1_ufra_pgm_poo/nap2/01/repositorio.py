# repositorio.py
# Esse arquivo cuida de salvar e carregar os dados em JSON (meu “banco de dados”).
# Basicamente serializa os objetos (itens, usuários, transações) em dicionários
# e depois reconstrói eles na hora de carregar.

import json
from pathlib import Path   # Path facilita manipular arquivos
from dominio import Livro, Revista, Dvd, Aluno, Professor, Visitante, Emprestimo, Devolucao

def salvar(caminho, itens, usuarios, transacoes):
    # função que transforma todos os objetos em dicionários e salva num JSON
    dados = {
        "itens": [i.para_dict() for i in itens],              # cada item vira dict
        "usuarios": [u.para_dict() for u in usuarios],        # cada usuário vira dict
        "transacoes": [t.para_dict() for t in transacoes],    # cada transação vira dict
    }
    # uso Path pra escrever direto o JSON no arquivo
    Path(caminho).write_text(json.dumps(dados, indent=2, ensure_ascii=False))

def carregar(caminho):
    # função que lê o arquivo JSON e reconstrói os objetos de volta
    p = Path(caminho)
    if not p.exists(): 
        # se não existir o arquivo, retorno 3 listas vazias
        return [], [], []
    dados = json.loads(p.read_text())   # leio e converto de JSON pra dict

    # ===== Reconstrução dos Itens =====
    itens = []
    for d in dados.get("itens", []):
        t = d.get("tipo")
        if t == "Livro":
            # Livro precisa de titulo, autor, e isbn (no dict tem isso)
            itens.append(Livro(
                d["titulo"], d["autor"], d["isbn"],
                id_=d["id"], status=d["status"], criado_em=d["criado_em"]
            ))
        elif t == "Revista":
            itens.append(Revista(
                d["titulo"], d["edicao"],
                id_=d["id"], status=d["status"], criado_em=d["criado_em"]
            ))
        elif t == "Dvd":
            itens.append(Dvd(
                d["titulo"], d["duracao_min"],
                id_=d["id"], status=d["status"], criado_em=d["criado_em"]
            ))

    # ===== Reconstrução dos Usuários =====
    usuarios = []
    for d in dados.get("usuarios", []):
        t = d.get("tipo")
        # preparo os kwargs que todas as classes precisam
        kw = dict(
            id_=d["id"], status=d["status"], 
            criado_em=d["criado_em"], emprestados=d.get("emprestados", 0)
        )
        if t == "Aluno": usuarios.append(Aluno(d["nome"], **kw))
        elif t == "Professor": usuarios.append(Professor(d["nome"], **kw))
        elif t == "Visitante": usuarios.append(Visitante(d["nome"], **kw))

    # ===== Reconstrução das Transações =====
    transacoes = []
    for d in dados.get("transacoes", []):
        t = d.get("tipo")
        kw = dict(id_=d["id"], status=d["status"], criado_em=d["criado_em"])
        if t == "Emprestimo":
            transacoes.append(Emprestimo(d["usuario_id"], d["item_id"], **kw))
        elif t == "Devolucao":
            transacoes.append(Devolucao(d["usuario_id"], d["item_id"], **kw))

    return itens, usuarios, transacoes


# ===== Teste rápido (só roda se eu chamar direto esse arquivo) =====
if __name__ == "__main__":
    itens, usuarios, transacoes = [], [], []
    # crio um livro de teste
    itens.append(Livro("Livro X", "Autora Y", "111"))
    # crio um aluno de teste
    usuarios.append(Aluno("Joao"))
    # salvo em JSON
    salvar("biblio.json", itens, usuarios, transacoes)
    # carrego de volta do arquivo
    i, u, t = carregar("biblio.json")
    print("Carregado:", len(i), len(u), len(t))  # só confiro os tamanhos
