
# ui_charts.py — Widgets de gráficos em Pygame (barras simples)
import pygame

def draw_bar_chart(surface, data, rect, title="Gráfico", value_key='value', label_key='label'):
    """
    Desenha um gráfico de barras.
    data: lista de dicts [{'label': 'Livro', 'value': 10}, ...]
    rect: pygame.Rect(x, y, w, h)
    """
    if not pygame.get_init(): pygame.init()
    if not pygame.font.get_init(): pygame.font.init()
    font_title = pygame.font.SysFont('Arial', 20, bold=True)
    font_lbl = pygame.font.SysFont('Arial', 14)

    x, y, w, h = rect
    pygame.draw.rect(surface, (250,250,252), rect, border_radius=10)
    pygame.draw.rect(surface, (220,220,230), rect, width=1, border_radius=10)

    title_s = font_title.render(title, True, (40,40,60))
    surface.blit(title_s, (x + 12, y + 8))
    if not data:
        nd = font_lbl.render("Sem dados", True, (120,120,130))
        surface.blit(nd, (x + w//2 - nd.get_width()//2, y + h//2 - nd.get_height()//2))
        return

    # área útil do gráfico
    gx, gy = x + 18, y + 38
    gw, gh = w - 36, h - 60

    max_v = max(max(0, d.get(value_key, 0)) for d in data)
    n = len(data)
    if n == 0 or max_v == 0:
        return

    bar_w = max(8, gw // (n * 2))
    gap = bar_w

    for i, d in enumerate(data):
        v = max(0, d.get(value_key, 0))
        lbl = str(d.get(label_key, ''))
        bh = int((v / max_v) * (gh - 20))
        bx = gx + i * (bar_w + gap)
        by = gy + gh - bh
        pygame.draw.rect(surface, (100,150,200), (bx, by, bar_w, bh), border_radius=6)
        # valor acima
        val_s = font_lbl.render(str(v), True, (50,50,60))
        surface.blit(val_s, (bx + bar_w//2 - val_s.get_width()//2, by - 16))
        # label embaixo
        lbl_s = font_lbl.render(lbl, True, (50,50,60))
        surface.blit(lbl_s, (bx + bar_w//2 - lbl_s.get_width()//2, gy + gh + 2))
