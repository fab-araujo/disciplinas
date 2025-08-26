# main.py
import pygame
import random
from animais import Dragao, Fenix

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Batalha de Animais Fantásticos")

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 28)
fonte_pequena = pygame.font.SysFont(None, 20)

def desenhar_texto(texto, posicao, cor=(255,255,255), fonte_texto=None):
    if fonte_texto is None:
        fonte_texto = fonte
    img = fonte_texto.render(texto, True, cor)
    tela.blit(img, posicao)

def desenhar_barra_cooldown(surface, x, y, cooldown_atual, cooldown_max, largura=100, altura=8):
    """Desenha uma barra de cooldown visual"""
    # Fundo da barra (cinza escuro)
    pygame.draw.rect(surface, (50, 50, 50), (x, y, largura, altura))
    
    # Barra de cooldown (azul)
    if cooldown_atual > 0:
        progresso = cooldown_atual / cooldown_max
        largura_barra = largura * progresso
        pygame.draw.rect(surface, (100, 100, 255), (x, y, largura_barra, altura))
    
    # Borda da barra
    pygame.draw.rect(surface, (200, 200, 200), (x, y, largura, altura), 1)

def main():
    jogador = Dragao("Draco")
    inimigo = Fenix("Fawkes")

    inimigo_timer = 60
    jogo_terminou = False  # Flag para controlar se o jogo terminou

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a and jogador.esta_vivo() and not jogo_terminou:
                    sucesso = jogador.atacar(inimigo)
                    if not sucesso:
                        print("Ataque em cooldown!")
                elif evento.key == pygame.K_h and jogador.esta_vivo() and not jogo_terminou:
                    sucesso = jogador.usar_habilidade(inimigo)
                    if not sucesso:
                        print("Habilidade em cooldown ou sem energia!")
                elif evento.key == pygame.K_r and jogo_terminou:
                    # Reinicia o jogo
                    jogador = Dragao("Draco")
                    inimigo = Fenix("Fawkes")
                    inimigo_timer = 60
                    jogo_terminou = False

        # IA simples do inimigo (só funciona se o jogo não terminou)
        if not jogo_terminou and inimigo.esta_vivo():
            inimigo_timer -= 1
            if inimigo_timer <= 0:
                if random.random() < 0.5:
                    sucesso = inimigo.atacar(jogador)
                    if not sucesso:
                        print(f"{inimigo.nome} tentou atacar mas está em cooldown!")
                else:
                    sucesso = inimigo.usar_habilidade(inimigo)  # Fênix se cura
                    if not sucesso:
                        print(f"{inimigo.nome} tentou usar habilidade mas está em cooldown!")
                inimigo_timer = 60

        # Verifica condições de fim de jogo
        if not jogo_terminou:
            if not jogador.esta_vivo():
                jogo_terminou = True
                # Para a regeneração dos personagens
                jogador.parar_regeneracao()
                inimigo.parar_regeneracao()
            elif not inimigo.esta_vivo():
                jogo_terminou = True
                # Para a regeneração dos personagens
                jogador.parar_regeneracao()
                inimigo.parar_regeneracao()

        tela.fill((30, 30, 30))
        
        # Desenha os personagens na posição final
        jogador.desenhar(tela, (200, 300))
        inimigo.desenhar(tela, (600, 300))

        # Informações dos personagens
        desenhar_texto(f"{jogador.nome} - Vida: {jogador.vida}/{jogador.vida_maxima} Energia: {jogador.energia}/{jogador.energia_maxima}", (50, 50))
        desenhar_texto(f"{inimigo.nome} - Vida: {inimigo.vida}/{inimigo.vida_maxima} Energia: {inimigo.energia}/{inimigo.energia_maxima}", (450, 50))
        
        # Barras de cooldown do jogador
        desenhar_texto("Cooldowns:", (50, 100), (200, 200, 50), fonte_pequena)
        desenhar_texto("Ataque:", (50, 120), (255, 100, 100), fonte_pequena)
        desenhar_barra_cooldown(tela, 50, 140, jogador.cooldown_ataque, jogador.cooldown_ataque_max)
        desenhar_texto("Habilidade:", (50, 160), (255, 215, 0), fonte_pequena)
        desenhar_barra_cooldown(tela, 50, 180, jogador.cooldown_habilidade, jogador.cooldown_habilidade_max)
        
        # Barras de cooldown do inimigo
        desenhar_texto("Cooldowns:", (450, 100), (200, 200, 50), fonte_pequena)
        desenhar_texto("Ataque:", (450, 120), (255, 100, 100), fonte_pequena)
        desenhar_barra_cooldown(tela, 450, 140, inimigo.cooldown_ataque, inimigo.cooldown_ataque_max)
        desenhar_texto("Habilidade:", (450, 160), (255, 215, 0), fonte_pequena)
        desenhar_barra_cooldown(tela, 450, 180, inimigo.cooldown_habilidade, inimigo.cooldown_habilidade_max)
        
        if not jogo_terminou:
            desenhar_texto("A=Atacar | H=Habilidade", (100, 550), (200,200,50))
        else:
            # Mostra mensagem de fim de jogo
            if not jogador.esta_vivo():
                desenhar_texto("VOCÊ FOI DERROTADO!", (300, 500), (255,0,0))
                desenhar_texto("Pressione R para reiniciar", (280, 530), (200,200,50))
            elif not inimigo.esta_vivo():
                desenhar_texto("VOCÊ VENCEU!", (320, 500), (0,255,0))
                desenhar_texto("Pressione R para reiniciar", (280, 530), (200,200,50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
