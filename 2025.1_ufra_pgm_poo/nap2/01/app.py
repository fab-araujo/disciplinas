# app.py (versão enxuta, agora bem comentado por mim)
# Objetivo: UI simples em Pygame pra gerenciar itens e usuários de uma biblioteca
# Fluxos principais: Menu -> (Gerenciar Empréstimos | Cadastrar Item | Cadastrar Usuário)

import sys, pygame
from dominio import Livro, Revista, Dvd, Aluno, Professor, Visitante
from servicos import criar_item, criar_usuario, processar_emprestimo, processar_devolucao, relatorio_disponiveis, relatorio_emprestados

# ====== Configs visuais básicas ======
LARG, ALT = 1000, 640                      # resolucao da janela (quero algo mais “widescreen”)
BRANCO, PRETO = (255,255,255), (0,0,0)     # cores que uso toda hora
AZUL, VERDE, VERMELHO, CINZA = (30,144,255), (0,170,0), (200,50,50), (80,80,80)  # paleta simples

# ====== Inicialização do pygame ======
pygame.init()
tela = pygame.display.set_mode((LARG, ALT))    # aqui eu crio a janela principal
pygame.display.set_caption("BiblioManager")    # nome bonitinho na barra de título
clock = pygame.time.Clock()                    # controle do FPS (quero ~60fps)
fonte_titulo = pygame.font.SysFont(None, 46)  # fontes: titulo maior
fonte = pygame.font.SysFont(None, 28)         # fonte padrão
fonte_peq = pygame.font.SysFont(None, 22)     # fonte menor (listas)

# ====== Fundo opcional (se imagem faltar, só pinto cor clara) ======
try:
    fundo = pygame.image.load("fundo1.png")                       # tento carregar imagem
    fundo = pygame.transform.scale(fundo, (LARG, ALT))            # garanto que preenche a area toda
except Exception:
    fundo = None                                                  # sem erro, só sem fundo

def fundo_draw():
    # funçãozinha pra desenhar fundo (ou cor fallback)
    if fundo: tela.blit(fundo, (0,0))
    else: tela.fill((240,244,248))  # um cinza/azulado leve como padrão

# ====== Componentes de UI simples: Botão e Input ======
class Botao:
    # botão bem simples: só um retângulo arredondado com texto central
    def __init__(self, rect, texto, cor, cor_txt=BRANCO):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.cor = cor
        self.cor_txt = cor_txt
    def desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=8)
        t = fonte.render(self.texto, True, self.cor_txt)
        tela.blit(t, (self.rect.centerx - t.get_width()//2, self.rect.centery - t.get_height()//2))
    def click(self, pos):
        # retorno booleano se clique bateu dentro do botão
        return self.rect.collidepoint(pos)

class Input:
    # input de texto básico (um campo por vez “ativo”)
    def __init__(self, x,y,w, placeholder=""):
        self.r = pygame.Rect(x,y,w,34)
        self.txt = ""
        self.act = False
        self.ph = placeholder  # placeholder pra lembrar o que digitar
    def draw(self):
        pygame.draw.rect(tela, BRANCO, self.r, border_radius=6)
        pygame.draw.rect(tela, CINZA, self.r, 1, border_radius=6)
        s = self.txt if self.txt else self.ph
        cor = PRETO if self.txt else (120,120,120)  # placeholder em cinza
        tela.blit(fonte.render(s, True, cor), (self.r.x+8, self.r.y+6))
    def handle(self, e):
        # foco via clique + digitação simples, sem seleção/clipboard (mantive enxuto)
        if e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            self.act = self.r.collidepoint(e.pos)
        if e.type==pygame.KEYDOWN and self.act:
            if e.key==pygame.K_BACKSPACE:
                self.txt = self.txt[:-1]         # apago ultimo caractere
            elif e.key==pygame.K_RETURN:
                self.act = False                 # enter tira foco (me ajuda a confirmar)
            else:
                if len(self.txt) < 60:          # limite pra nao explodir layout
                    self.txt += e.unicode

# ====== Estados de tela (máquina de estados bem direta) ======
TELA_MENU, TELA_GER, TELA_ITEM, TELA_USER = "menu","ger","item","user"
tela_atual = TELA_MENU  # começo sempre no menu

# ====== “Banco de dados” em memória (prototipo mesmo) ======
itens = [Livro("Python","Guido"), Livro("Algoritmos","Wirth"), Revista("Ciencia Hoje","102"), Dvd("Interstellar",169)]
usuarios = [Aluno("Ana")]    # deixo uma usuaria inicial pra testar o fluxo rápido
transacoes = []              # registro bruto das operações (usado pelos serviços)
sel_user, sel_item = 0, -1   # seleções padrão: já aponto 1º usuário, item nenhum

# ====== Botões do menu e áreas de listagem ======
b_menu_ger = Botao((370,220,260,50),"Gerenciar Emprestimos", VERDE)
b_menu_item= Botao((370,290,260,50),"Cadastrar Item", AZUL)
b_menu_user= Botao((370,360,260,50),"Cadastrar Usuario", AZUL)
b_menu_sair= Botao((370,430,260,50),"Sair", VERMELHO)
b_voltar   = Botao((20,20,120,36),"Voltar", CINZA)

b_emp = Botao((40,100,180,40),"Emprestar", VERDE)
b_dev = Botao((40,150,180,40),"Devolver", VERMELHO)
area_users = pygame.Rect(260,90,380,480)   # painel com a lista de usuários
area_itens = pygame.Rect(660,90,300,480)   # painel com a lista de itens

# ====== Cadastro de Item (abas por tipo) ======
tipos_item = ["Livro","Revista","Dvd"]; idx_item = 0  # começo pela aba “Livro”
i_titulo = Input(80,180,360,"titulo")
i_autor  = Input(80,230,360,"autor (Livro)")
i_edicao = Input(80,230,360,"edicao (Revista)")
i_dur    = Input(80,230,360,"duracao em minutos (Dvd)")
b_cad_item = Botao((80,300,200,44),"Cadastrar", AZUL)

# ====== Cadastro de Usuário (abas por tipo) ======
tipos_user = ["Aluno","Professor","Visitante"]; idx_user = 0
i_nome = Input(80,200,360,"nome do usuario")
b_cad_user = Botao((80,260,200,44),"Cadastrar", AZUL)

# ====== Helper pra desenhar texto (pra evitar repetir render) ======
def texto(s,x,y, f=fonte, cor=PRETO):
    tela.blit(f.render(s, True, cor), (x,y))

# ====== Telas: Menu ======
def desenhar_menu():
    fundo_draw()
    texto("BiblioManager", 380,140, fonte_titulo, AZUL)
    for b in (b_menu_ger,b_menu_item,b_menu_user,b_menu_sair):
        b.desenhar()

# ====== Telas: Gerenciar Empréstimos ======
def desenhar_ger():
    fundo_draw()
    b_voltar.desenhar()
    texto("Gerenciar Emprestimos", 320,32, fonte_titulo, AZUL)

    # botoes ação
    b_emp.desenhar()
    b_dev.desenhar()

    # painel usuários (nome em verde + quantos itens cada um tem)
    pygame.draw.rect(tela, BRANCO, area_users, border_radius=8)
    pygame.draw.rect(tela, CINZA, area_users, 1, border_radius=8)
    texto("Usuarios", area_users.x+10, area_users.y+8, fonte, CINZA)
    y = area_users.y+38
    for i,u in enumerate(usuarios):
        r = pygame.Rect(area_users.x+8, y, area_users.w-16, 28)
        if i==sel_user:
            pygame.draw.rect(tela, (220,240,255), r, border_radius=6)  # destaque do selecionado
        texto(u.nome, r.x+8, r.y+5, fonte_peq, VERDE)
        texto(f"({u.emprestados})", r.x+160, r.y+5, fonte_peq, PRETO)
        y += 30

    # painel itens (mostro título, status e recorto id pra ficar curtinho)
    pygame.draw.rect(tela, BRANCO, area_itens, border_radius=8)
    pygame.draw.rect(tela, CINZA, area_itens, 1, border_radius=8)
    texto("Itens", area_itens.x+10, area_itens.y+8, fonte, CINZA)
    y = area_itens.y+38
    for i,it in enumerate(itens):
        r = pygame.Rect(area_itens.x+8, y, area_itens.w-16, 28)
        if i==sel_item:
            pygame.draw.rect(tela, (220,255,220), r, border_radius=6)  # destaque do selecionado
        texto(f"{it.titulo} | {it.status} | id={it.id[:8]}", r.x+8, r.y+5, fonte_peq, PRETO)
        y += 30

# ====== Telas: Cadastro de Item ======
def desenhar_item():
    fundo_draw()
    b_voltar.desenhar()
    texto("Cadastrar Item", 380,32, fonte_titulo, AZUL)

    # abas de tipo (parecem “tabs”)
    base_x = 80
    for i,t in enumerate(tipos_item):
        r = pygame.Rect(base_x+i*120, 100, 110, 36)
        pygame.draw.rect(tela, AZUL if i==idx_item else CINZA, r, border_radius=8)
        texto(t, r.x+18, r.y+7, fonte, BRANCO)

    # inputs por tipo (só mostro o que faz sentido)
    i_titulo.draw()
    tipo = tipos_item[idx_item]
    if tipo == "Livro":
        i_autor.draw()
    elif tipo == "Revista":
        i_edicao.draw()
    else:
        i_dur.draw()
    b_cad_item.desenhar()

    # painel lateral listando últimos cadastrados (só pra ter feedback visual)
    painel = pygame.Rect(520,100,420,420)
    pygame.draw.rect(tela, BRANCO, painel, border_radius=8)
    pygame.draw.rect(tela, CINZA, painel, 1, border_radius=8)
    texto("Itens cadastrados", painel.x+10, painel.y+8, fonte, CINZA)
    y = painel.y+40
    for it in itens[-12:][::-1]:
        texto(f"- {it.titulo} | {it.status} | id={it.id[:8]}", painel.x+10, y, fonte_peq, PRETO)
        y += 24

# ====== Telas: Cadastro de Usuário ======
def desenhar_user():
    fundo_draw()
    b_voltar.desenhar()
    texto("Cadastrar Usuario", 360,32, fonte_titulo, AZUL)

    # abas por tipo de usuário
    base_x = 80
    for i,t in enumerate(tipos_user):
        r = pygame.Rect(base_x+i*140, 100, 130, 36)
        pygame.draw.rect(tela, AZUL if i==idx_user else CINZA, r, border_radius=8)
        texto(t, r.x+20, r.y+7, fonte, BRANCO)

    # input do nome + botão
    i_nome.draw()
    b_cad_user.desenhar()

    # painel lateral com últimos usuários (só pra ver que foi)
    painel = pygame.Rect(520,100,420,420)
    pygame.draw.rect(tela, BRANCO, painel, border_radius=8)
    pygame.draw.rect(tela, CINZA, painel, 1, border_radius=8)
    texto("Usuarios cadastrados", painel.x+10, painel.y+8, fonte, CINZA)
    y = painel.y+40
    for u in usuarios[-12:][::-1]:
        texto(f"- {u.nome} ({u.emprestados}) id={u.id[:8]}", painel.x+10, y, fonte_peq, PRETO)
        y += 24

# ====== Loop principal (eventos + desenho) ======
def main():
    # uso “global” porque altero seleções/abas dentro do loop de eventos
    global tela_atual, sel_user, sel_item, idx_item, idx_user
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # fechei a janela => saio bonito
                pygame.quit()
                sys.exit()

            # ===== Inputs ativos por tela =====
            if tela_atual == TELA_ITEM:
                # só lido com inputs dos itens quando estou nessa tela
                for inp in (i_titulo, i_autor, i_edicao, i_dur):
                    inp.handle(e)
            if tela_atual == TELA_USER:
                i_nome.handle(e)

            # ===== Cliques do mouse =====
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos

                # ----- Menu -----
                if tela_atual == TELA_MENU:
                    if b_menu_ger.click((mx,my)): 
                        tela_atual = TELA_GER
                        # dica: quando entro em GER, mantenho seleções (facilita testar emprestimo)
                    elif b_menu_item.click((mx,my)): 
                        tela_atual = TELA_ITEM
                    elif b_menu_user.click((mx,my)): 
                        tela_atual = TELA_USER
                    elif b_menu_sair.click((mx,my)): 
                        pygame.quit(); sys.exit()

                # ----- Gerenciar Empréstimos -----
                elif tela_atual == TELA_GER:
                    if b_voltar.click((mx,my)):
                        tela_atual = TELA_MENU
                    elif b_emp.click((mx,my)):
                        # regra do empréstimo: preciso ter user e item selecionados e item disponível
                        if sel_user != -1 and sel_item != -1 and itens[sel_item].status == "disponivel":
                            u = usuarios[sel_user]
                            it = itens[sel_item]
                            # chamo a função de serviço (ela atualiza listas e registra transação)
                            processar_emprestimo(usuarios, itens, transacoes, u.id, it.id)
                    elif b_dev.click((mx,my)):
                        # devolução: similar, mas item precisa estar emprestado
                        if sel_user != -1 and sel_item != -1 and itens[sel_item].status == "emprestado":
                            u = usuarios[sel_user]
                            it = itens[sel_item]
                            processar_devolucao(usuarios, itens, transacoes, u.id, it.id)

                    # clique dentro da área de usuários => calculo “linha” clicada
                    if area_users.collidepoint((mx,my)):
                        lin = (my - (area_users.y + 38)) // 30
                        if 0 <= lin < len(usuarios):
                            sel_user = lin
                    # clique dentro da área de itens
                    if area_itens.collidepoint((mx,my)):
                        lin = (my - (area_itens.y + 38)) // 30
                        if 0 <= lin < len(itens):
                            sel_item = lin

                # ----- Cadastro de Item -----
                elif tela_atual == TELA_ITEM:
                    if b_voltar.click((mx,my)):
                        # ao voltar, limpo campos e retorno ao menu
                        i_titulo.txt = i_autor.txt = i_edicao.txt = i_dur.txt = ""
                        tela_atual = TELA_MENU

                    # clique nas abas de tipo de item (Livro/Revista/Dvd)
                    base_x = 80
                    for i in range(len(tipos_item)):
                        r = pygame.Rect(base_x+i*120, 100, 110, 36)
                        if r.collidepoint((mx,my)):
                            idx_item = i
                            # troquei de aba => limpo inputs pra não confundir
                            i_titulo.txt = i_autor.txt = i_edicao.txt = i_dur.txt = ""
                            break

                    # botão cadastrar item
                    if b_cad_item.click((mx,my)):
                        titulo = i_titulo.txt.strip()
                        if not titulo:
                            # se não tem título, eu simplesmente ignoro (continue)
                            # (poderia mostrar um aviso visual, mas mantive simples)
                            continue
                        t = tipos_item[idx_item]
                        if t == "Livro":
                            autor = i_autor.txt.strip()
                            if autor:
                                criar_item(itens, Livro(titulo, autor))
                                i_titulo.txt = i_autor.txt = ""
                        elif t == "Revista":
                            ed = i_edicao.txt.strip()
                            if ed:
                                criar_item(itens, Revista(titulo, ed))
                                i_titulo.txt = i_edicao.txt = ""
                        else:
                            d = i_dur.txt.strip()
                            # garantia de que é número inteiro em minutos
                            if d.isdigit():
                                criar_item(itens, Dvd(titulo, int(d)))
                                i_titulo.txt = i_dur.txt = ""

                # ----- Cadastro de Usuário -----
                elif tela_atual == TELA_USER:
                    if b_voltar.click((mx,my)):
                        i_nome.txt = ""
                        tela_atual = TELA_MENU

                    # abas de tipo de usuário
                    base_x = 80
                    for i in range(len(tipos_user)):
                        r = pygame.Rect(base_x+i*140, 100, 130, 36)
                        if r.collidepoint((mx,my)):
                            idx_user = i
                            i_nome.txt = ""
                            break

                    # botão cadastrar usuário
                    if b_cad_user.click((mx,my)):
                        nome = i_nome.txt.strip()
                        if not nome:
                            # sem nome não crio (mesmo esquema de cima)
                            continue
                        t = tipos_user[idx_user]
                        if t == "Aluno":
                            criar_usuario(usuarios, Aluno(nome))
                        elif t == "Professor":
                            criar_usuario(usuarios, Professor(nome))
                        else:
                            criar_usuario(usuarios, Visitante(nome))
                        i_nome.txt = ""

        # ===== Desenho da tela conforme estado atual =====
        if tela_atual == TELA_MENU:
            desenhar_menu()
        elif tela_atual == TELA_GER:
            desenhar_ger()
        elif tela_atual == TELA_ITEM:
            desenhar_item()
        elif tela_atual == TELA_USER:
            desenhar_user()

        # flip final + trava de FPS (pra não fritar CPU)
        pygame.display.flip()
        clock.tick(60)

# ====== Ponto de entrada padrão ======
if __name__ == "__main__":
    # regra geral que sempre uso: só roda main se for executado diretamente
    main()
