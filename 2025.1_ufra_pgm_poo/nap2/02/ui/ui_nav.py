
# ui_nav.py — utilitário para botão "Sair"
import pygame

def draw_exit_button(surface, x, y, label="Sair"):
    if not pygame.get_init(): pygame.init()
    if not pygame.font.get_init(): pygame.font.init()
    font = pygame.font.SysFont('Arial', 16)
    r = pygame.Rect(x, y, 90, 32)
    pygame.draw.rect(surface, (220,80,80), r, border_radius=8)
    txt = font.render(label, True, (255,255,255))
    surface.blit(txt, (r.centerx - txt.get_width()//2, r.centery - txt.get_height()//2))
    return r
