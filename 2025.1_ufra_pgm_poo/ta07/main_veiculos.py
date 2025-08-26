# main.py
import pygame
from pessoas import Aluno

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Gerenciamento de Alunos")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 28)

# Lista de alunos
alunos = [
    Aluno("Alice", 20, "A001", "Engenharia"),
    Aluno("Bob", 22, "A002", "Matemática")
]

selecionado = 0
mensagem = ""
modo_input = False
input_campo = ""
input_tipo = ""  # "nome", "idade", "matricula", "curso"
editar_aluno = None

def desenhar_texto(texto, posicao, cor=(255,255,255)):
    img = fonte.render(texto, True, cor)
    tela.blit(img, posicao)

def main():
    global selecionado, mensagem, modo_input, input_campo, input_tipo, editar_aluno
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if modo_input:
                    if evento.key == pygame.K_RETURN:
                        # Salvar input
                        valor = input_campo
                        if input_tipo == "nome":
                            editar_aluno.nome = valor
                        elif input_tipo == "idade":
                            try:
                                editar_aluno.idade = int(valor)
                            except:
                                mensagem = "Idade inválida!"
                        elif input_tipo == "matricula":
                            editar_aluno._Aluno__matricula = valor
                        elif input_tipo == "curso":
                            editar_aluno._Aluno__curso = valor
                        modo_input = False
                        input_campo = ""
                        mensagem = f"{editar_aluno.nome} atualizado!"
                    elif evento.key == pygame.K_BACKSPACE:
                        input_campo = input_campo[:-1]
                    else:
                        input_campo += evento.unicode
                else:
                    if evento.key == pygame.K_DOWN:
                        selecionado = (selecionado + 1) % len(alunos)
                    elif evento.key == pygame.K_UP:
                        selecionado = (selecionado - 1) % len(alunos)
                    elif evento.key == pygame.K_RETURN:
                        mensagem = alunos[selecionado].acao_especial()
                    elif evento.key == pygame.K_a:  # Adicionar novo aluno
                        novo = Aluno("Novo Aluno", 18, f"A{len(alunos)+1:03}", "Curso X")
                        alunos.append(novo)
                        mensagem = f"{novo.nome} adicionado."
                    elif evento.key == pygame.K_e:  # Editar aluno
                        editar_aluno = alunos[selecionado]
                        modo_input = True
                        input_campo = ""
                        input_tipo = "nome"  # Pode criar seleção de campo depois
                        mensagem = f"Editando {editar_aluno.nome} - insira o novo nome e pressione Enter"
                    elif evento.key == pygame.K_d:  # Deletar aluno
                        excluido = alunos.pop(selecionado)
                        mensagem = f"{excluido.nome} removido."
                        selecionado = 0

        tela.fill((30,30,30))
        for i, a in enumerate(alunos):
            cor = (0,255,0) if i == selecionado else (255,255,255)
            desenhar_texto(a.exibir_informacoes(), (50, 50 + i*40), cor)

        desenhar_texto("↑/↓ Selecionar | Enter=Ação | A=Adicionar | E=Editar | D=Deletar", (50, 550), (200,200,50))
        desenhar_texto(mensagem, (50, 520), (255,200,0))
        if modo_input:
            desenhar_texto(f"Novo valor ({input_tipo}): {input_campo}", (50, 500), (255,255,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
