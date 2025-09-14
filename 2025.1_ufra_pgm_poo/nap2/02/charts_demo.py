
# charts_demo.py — demonstração isolada dos gráficos
import pygame
from ui_charts import draw_bar_chart

pygame.init(); pygame.font.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()

data_types = [{'label':'Livro','value':20},{'label':'Revista','value':15},{'label':'DVD','value':10}]
data_status = [{'label':'Disp.','value':40},{'label':'Emp.','value':5},{'label':'Res.','value':3}]
data_users = [{'label':'ST01','value':4},{'label':'PR01','value':7},{'label':'VI01','value':2}]

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False

    screen.fill((245,246,250))
    draw_bar_chart(screen, data_types, pygame.Rect(30,30,260,220), title="Itens por Tipo")
    draw_bar_chart(screen, data_status, pygame.Rect(320,30,260,220), title="Status dos Itens")
    draw_bar_chart(screen, data_users, pygame.Rect(610,30,260,220), title="Uso por Usuário")
    pygame.display.flip(); clock.tick(60)

pygame.quit()
