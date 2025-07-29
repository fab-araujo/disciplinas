# 1 - Importar as bibliotecas necessárias
import pygame
from pygame.locals import *
import sys

# 2 - Definir constantes
BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# 3 - Inicializar o pygame e criar a janela
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
 
# 4 - Carregar recursos (se necessário) - imagens, sons, etc.
ballImage = pygame.image.load('images/ball.png')

# 5 - Inicializar variáveis e objetos
x = 0
y = 0
 
# 6 - Loop principal do jogo
while True:

    # 7 - Verificar eventos
    for event in pygame.event.get():
        # Evento que fecha a janela
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()

    # 8 - Fazer qualquer ação por frame
    
    # 9 - Limpar a tela
    window.fill(BLACK)
    
    # 10 - Desenhar todos os objetos na tela
    x = x + 1
    y = y + 1
    window.blit(ballImage, (x, y))

    # 11 - Atualizar a tela
    pygame.display.update()

