# 1 - Importar as bibliotecas necessárias
import pygame
from pygame.locals import *
import sys
import random

# 2 - Definir constantes
BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
BALL_WIDTH_HEIGHT = 100
MAX_WIDTH = WINDOW_WIDTH - BALL_WIDTH_HEIGHT
MAX_HEIGHT = WINDOW_HEIGHT - BALL_WIDTH_HEIGHT

# 3 - Inicializar o pygame e criar a janela
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
 
# 4 - Carregar recursos (se necessário) - imagens, sons, etc.
ballImage = pygame.image.load('images/ball.png')

# 5 - Inicializar variáveis e objetos
ballX = random.randrange(MAX_WIDTH)
ballY = random.randrange(MAX_HEIGHT)
ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)
 
# 6 - Loop principal do jogo
while True:

    # 7 - Verificar eventos
    for event in pygame.event.get():
        # Evento que fecha a janela
        if event.type == pygame.QUIT:           
            pygame.quit()  
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            if ballRect.collidepoint(event.pos):
                ballX = random.randrange(MAX_WIDTH)
                ballY = random.randrange(MAX_HEIGHT)
                ballRect = pygame.Rect(ballX, ballY, BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT)

    # 8 - Fazer qualquer ação por frame
    
    # 9 - Limpar a tela
    window.fill(BLACK)
    
    # 10 - Desenhar todos os objetos na tela
    window.blit(ballImage, (ballX, ballY))

    # 11 - Atualizar a tela
    pygame.display.update()

    #12 - Controlar a taxa de frames
    clock.tick(FRAMES_PER_SECOND)

