import pygame
from abc import ABC, abstractmethod
from datetime import datetime

class TextBox:
    def __init__(self, x, y, w, h, font, prompt=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (200, 200, 200)
        self.color_active = (80, 200, 120)
        self.color = self.color_inactive
        self.text = ""
        self.font = font
        self.active = False
        self.prompt = prompt

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 50:
                    self.text += event.unicode
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        txt_surface = self.font.render(self.prompt + self.text, True, (30, 30, 30))
        screen.blit(txt_surface, (self.rect.x+10, self.rect.y+10))

    def get_text(self):
        return self.text

# --- Classes base (POO) ---
class LibraryEntity(ABC):
    def __init__(self, entity_id, name):
        self._id = entity_id
        self._name = name
        self._created_at = datetime.now()
        self._status = "active"

    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def status(self): return self._status
    @status.setter
    def status(self, new_status): self._status = new_status

    @abstractmethod
    def display_info(self): pass
    @abstractmethod
    def update_status(self, new_status): pass
    @abstractmethod
    def validate(self): pass
    @abstractmethod
    def serialize(self): pass

class Item(LibraryEntity, ABC):
    def __init__(self, entity_id, name):
        super().__init__(entity_id, name)
        self._available = True
    @property
    def available(self): return self._available
    @available.setter
    def available(self, value): self._available = value
    def update_status(self, new_status): self._available = (new_status == "available")

class Book(Item):
    def __init__(self, entity_id, name, isbn, authors):
        super().__init__(entity_id, name)
        self._isbn = isbn
        self._authors = authors
    def display_info(self): return f"Livro: {self.name} | ISBN: {self._isbn} | Autores: {', '.join(self._authors)}"
    def validate(self): return bool(self._isbn and self._authors)
    def serialize(self): return {"type": "Book", "id": self.id, "name": self.name, "isbn": self._isbn, "authors": self._authors, "available": self.available}

class Magazine(Item):
    def __init__(self, entity_id, name, edition):
        super().__init__(entity_id, name)
        self._edition = edition
    def display_info(self): return f"Revista: {self.name} | Edição: {self._edition}"
    def validate(self): return bool(self._edition)
    def serialize(self): return {"type": "Magazine", "id": self.id, "name": self.name, "edition": self._edition, "available": self.available}

class DVD(Item):
    def __init__(self, entity_id, name, duration):
        super().__init__(entity_id, name)
        self._duration = duration
    def display_info(self): return f"DVD: {self.name} | Duração: {self._duration} min"
    def validate(self): return self._duration > 0
    def serialize(self): return {"type": "DVD", "id": self.id, "name": self.name, "duration": self._duration, "available": self.available}

class User(LibraryEntity, ABC):
    def __init__(self, entity_id, name):
        super().__init__(entity_id, name)
        self._loans = []
    @property
    def loans(self): return self._loans
    def add_loan(self, loan): self._loans.append(loan)

class Student(User):
    def __init__(self, entity_id, name, max_loans=3):
        super().__init__(entity_id, name)
        self._max_loans = max_loans
    def display_info(self): return f"Aluno: {self.name} | Empréstimos: {len(self.loans)}/{self._max_loans}"
    def validate(self): return len(self.loans) < self._max_loans
    def serialize(self): return {"type": "Student", "id": self.id, "name": self.name, "loans": [loan.serialize() for loan in self.loans]}
    def update_status(self, new_status): self.status = new_status
    
class Professor(User):
    def display_info(self): return f"Professor: {self.name} | Empréstimos: {len(self.loans)}"
    def validate(self): return True
    def serialize(self): return {"type": "Professor", "id": self.id, "name": self.name, "loans": [loan.serialize() for loan in self.loans]}
    def update_status(self, new_status): self.status = new_status

class Visitor(User):
    def display_info(self): return f"Visitante: {self.name} | Empréstimos: {len(self.loans)}"
    def validate(self): return len(self.loans) == 0
    def serialize(self): return {"type": "Visitor", "id": self.id, "name": self.name, "loans": []}
    def update_status(self, new_status): self.status = new_status

class Transaction(LibraryEntity, ABC):
    def __init__(self, entity_id, name):
        super().__init__(entity_id, name)
    @abstractmethod
    def process(self, user, item): pass

class Loan(Transaction):
    def __init__(self, entity_id, user, item):
        super().__init__(entity_id, "Loan")
        self._user = user
        self._item = item
        self._date = datetime.now()
    def display_info(self): return f"Empréstimo: {self._user.name} -> {self._item.name} em {self._date.strftime('%d/%m/%Y')}"
    def validate(self): return self._item.available and self._user.validate()
    def process(self, user, item):
        if item.available and user.validate():
            item.available = False
            user.add_loan(self)
            return True
        return False
    def serialize(self): return {"type": "Loan", "user_id": self._user.id, "item_id": self._item.id, "date": self._date.isoformat()}
    def update_status(self, new_status): self.status = new_status

class Return(Transaction):
    def __init__(self, entity_id, user, item):
        super().__init__(entity_id, "Return")
        self._user = user
        self._item = item
        self._date = datetime.now()
    def display_info(self): return f"Devolução: {self._user.name} -> {self._item.name} em {self._date.strftime('%d/%m/%Y')}"
    def validate(self): return not self._item.available
    def process(self, user, item):
        item.available = True
        user.loans[:] = [loan for loan in user.loans if loan._item != item]
        return True
    def serialize(self): return {"type": "Return", "user_id": self._user.id, "item_id": self._item.id, "date": self._date.isoformat()}
    def update_status(self, new_status): self.status = new_status

# --- Dados da biblioteca ---
items = []
users = []
loans = []

# --- Funções de CRUD ---
def add_item(item): items.append(item)
def remove_item(item_id): global items; items = [i for i in items if i.id != item_id]
def add_user(user): users.append(user)
def remove_user(user_id): global users; users = [u for u in users if u.id != user_id]
def process_loan(user, item):
    loan = Loan(len(loans)+1, user, item)
    if loan.process(user, item):
        loans.append(loan)
        return True
    return False
def process_return(user, item):
    ret = Return(len(loans)+1, user, item)
    if ret.process(user, item): return True
    return False

# --- Interface Gráfica ---
WIDTH, HEIGHT = 1024, 768
WHITE = (240,240,240)
GRAY = (200,200,200)
GREEN = (80,200,120)
RED = (220,80,80)
BLACK = (30,30,30)
FONT_SIZE = 28

def draw_button(screen, text, x, y, w, h, color, font):
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x+20, y+(h-label.get_height())//2))

def main_menu(screen, font):
    buttons = [
        ("Adicionar Item", 60, 100),
        ("Remover Item", 60, 180),
        ("Cadastrar Usuário", 60, 260),
        ("Remover Usuário", 60, 340),
        ("Empréstimos", 60, 420),
        ("Devoluções", 60, 500),
        ("Relatórios", 60, 580),
        ("Estatísticas", 60, 660),
        ("Sair", 800, 700)
    ]
    for text, x, y in buttons:
        draw_button(screen, text, x, y, 320, 60, GRAY, font)

def render_text_in_rect(screen, info, font, color, x, y, box_width, box_height):
    min_font_size = 12
    font_size = font.get_height()
    render_font = pygame.font.SysFont("Arial", font_size)
    txt_surface = render_font.render(info, True, color)
    while txt_surface.get_width() > box_width - 24 and font_size > min_font_size:
        font_size -= 2
        render_font = pygame.font.SysFont("Arial", font_size)
        txt_surface = render_font.render(info, True, color)
    screen.blit(txt_surface, (x+12, y+(box_height-txt_surface.get_height())//2))

def item_shelf(screen, font, start_y=100, scroll_y=0):
    # Centralizado, não invade campos de texto
    x, y = 420, start_y + scroll_y
    box_width = 540
    box_height = 50
    for idx, item in enumerate(items):
        color = GREEN if item.available else RED
        pygame.draw.rect(screen, color, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Item {idx+1} (ID {item.id}): {item.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

def user_list(screen, font, start_y=100, scroll_y=0):
    # Centralizado, não invade campos de texto
    x, y = 420, start_y + scroll_y
    box_width = 540
    box_height = 50
    for idx, user in enumerate(users):
        pygame.draw.rect(screen, GRAY, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Usuário {idx+1} (ID {user.id}): {user.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

def report_screen(screen, font, start_y=100, scroll_y=0):
    y = start_y + scroll_y
    box_width = 900
    box_height = 40
    for idx, item in enumerate(items):
        info = f"{idx+1}. {item.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, 60, y+idx*40, box_width, box_height)

def stats_screen(screen, font):
    box_width = 540
    box_height = 50
    label1 = f"Total de itens: {len(items)}"
    label2 = f"Disponíveis: {sum(1 for i in items if i.available)}"
    label3 = f"Emprestados: {len(items) - sum(1 for i in items if i.available)}"
    render_text_in_rect(screen, label1, font, BLACK, 60, 100, box_width, box_height)
    render_text_in_rect(screen, label2, font, GREEN, 60, 160, box_width, box_height)
    render_text_in_rect(screen, label3, font, RED, 60, 220, box_width, box_height)

def item_shelf_select(screen, font, selectable_items, selected_idx, start_y=100, scroll_y=0):
    x, y = 420, start_y + scroll_y
    box_width = 540
    box_height = 50
    for idx, item in enumerate(selectable_items):
        color = GREEN if item.available else RED
        if idx == selected_idx:
            pygame.draw.rect(screen, (255, 255, 0), (x-5, y+idx*60-5, box_width+10, box_height+10), border_radius=10)
        pygame.draw.rect(screen, color, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Item {idx+1} (ID {item.id}): {item.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

def user_list_select(screen, font, selectable_users, selected_idx, start_y=100, scroll_y=0):
    x, y = 420, start_y + scroll_y
    box_width = 540
    box_height = 50
    for idx, user in enumerate(selectable_users):
        if idx == selected_idx:
            pygame.draw.rect(screen, (255, 255, 0), (x-5, y+idx*60-5, box_width+10, box_height+10), border_radius=10)
        pygame.draw.rect(screen, GRAY, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Usuário {idx+1} (ID {user.id}): {user.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

# Para as listas laterais das telas de empréstimo e devolução:
def user_list_left(screen, font, start_y=380, scroll_y=0):
    # Lateral esquerda
    x, y = 40, start_y + scroll_y
    box_width = 400
    box_height = 50
    for idx, user in enumerate(users):
        pygame.draw.rect(screen, GRAY, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Usuário {idx+1} (ID {user.id}): {user.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

def item_shelf_right(screen, font, items_to_show, start_y=380, scroll_y=0):
    # Lateral direita
    box_width = 400
    box_height = 50
    x = WIDTH - box_width - 40
    y = start_y + scroll_y
    for idx, item in enumerate(items_to_show):
        color = GREEN if item.available else RED
        pygame.draw.rect(screen, color, (x, y+idx*60, box_width, box_height), border_radius=8)
        info = f"Item {idx+1} (ID {item.id}): {item.display_info()}"
        render_text_in_rect(screen, info, font, BLACK, x, y+idx*60, box_width, box_height)

def loan_report(screen, font, start_y=100, scroll_y=0):
    y = start_y + scroll_y
    box_width = 900
    box_height = 40
    for idx, loan in enumerate(loans):
        user_id = loan._user.id
        item_id = loan._item.id
        info = f"Empréstimo: Usuário {user_id} ({loan._user.name}) -> Item {item_id} ({loan._item.name}) em {loan._date.strftime('%d/%m/%Y')}"
        render_text_in_rect(screen, info, font, BLACK, 60, y+idx*40, box_width, box_height)

def return_report(screen, font, start_y=100, scroll_y=0):
    y = start_y + scroll_y
    box_width = 900
    box_height = 40
    for idx, ret in enumerate([l for l in loans if not l._item.available]):
        user_id = ret._user.id
        item_id = ret._item.id
        info = f"Devolução: Usuário {user_id} ({ret._user.name}) -> Item {item_id} ({ret._item.name})"
        render_text_in_rect(screen, info, font, BLACK, 60, y+idx*40, box_width, box_height)

def main():
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("BiblioManager")
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    clock = pygame.time.Clock()
    state = "menu"

    add_item(Book(1, "POO em Python", "123456", ["Fabrício"]))
    add_item(Magazine(2, "Ciência Hoje", "Edição 2025"))
    add_item(DVD(3, "Matrix", 120))
    add_user(Student(1, "Ana"))
    add_user(Professor(2, "Carlos"))
    add_user(Visitor(3, "João"))

    next_item_id = 4
    next_user_id = 4

    selected_user_idx = 0
    selected_item_idx = 0

    # Scroll variables
    scroll_y_items = 0
    scroll_y_users = 0
    scroll_y_report = 0
    scroll_speed = 40

    # Caixas de texto para cada tela (com espaçamento maior)
    user_boxes = [
        TextBox(200, 200, 400, 50, font, "Nome: "),
        TextBox(200, 280, 400, 50, font, "Tipo (Aluno/Professor/Visitante): ")
    ]
    item_boxes = [
        TextBox(200, 200, 400, 50, font, "Nome: "),
        TextBox(200, 280, 400, 50, font, "Tipo (Livro/Revista/DVD): "),
        TextBox(200, 360, 400, 50, font, "Info extra (ISBN/Edição/Duração): "),
        TextBox(200, 440, 400, 50, font, "Autores (se Livro): ")
    ]
    remove_user_box = TextBox(200, 200, 400, 50, font, "ID do usuário para remover: ")
    remove_item_box = TextBox(200, 200, 400, 50, font, "ID do item para remover: ")
    loan_boxes = [
        TextBox(200, 200, 400, 50, font, "ID do usuário: "),
        TextBox(200, 280, 400, 50, font, "ID do item disponível: ")
    ]
    return_boxes = [
        TextBox(200, 200, 400, 50, font, "ID do usuário: "),
        TextBox(200, 280, 400, 50, font, "ID do item emprestado: ")
    ]

    while True:
        screen.fill(WHITE)

        title_font = pygame.font.SysFont("Arial", 40, bold=True)
        title_text = title_font.render("BiblioManager", True, BLACK)
        screen.blit(title_text, (WIDTH - title_text.get_width() - 40, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # --- SCROLL EVENTS ---
            if event.type == pygame.KEYDOWN:
                if state in ["menu", "add_item", "remove_item"]:
                    if event.key == pygame.K_DOWN:
                        scroll_y_items -= scroll_speed
                    elif event.key == pygame.K_UP:
                        scroll_y_items += scroll_speed
                if state in ["add_user", "remove_user"]:
                    if event.key == pygame.K_DOWN:
                        scroll_y_users -= scroll_speed
                    elif event.key == pygame.K_UP:
                        scroll_y_users += scroll_speed
                if state == "report":
                    if event.key == pygame.K_DOWN:
                        scroll_y_report -= scroll_speed
                    elif event.key == pygame.K_UP:
                        scroll_y_report += scroll_speed
            if event.type == pygame.MOUSEWHEEL:
                if state in ["menu", "add_item", "remove_item"]:
                    scroll_y_items += event.y * scroll_speed
                if state in ["add_user", "remove_user"]:
                    scroll_y_users += event.y * scroll_speed
                if state == "report":
                    scroll_y_report += event.y * scroll_speed

            # --- LIMIT SCROLL ---
            max_items = len(items)
            max_users = len(users)
            max_report = len(items)
            visible_items = (HEIGHT - 100) // 70
            visible_users = (HEIGHT - 100) // 70
            visible_report = (HEIGHT - 100) // 40
            min_scroll_items = min(0, HEIGHT - 100 - max_items*70)
            min_scroll_users = min(0, HEIGHT - 100 - max_users*70)
            min_scroll_report = min(0, HEIGHT - 100 - max_report*40)
            scroll_y_items = max(min(scroll_y_items, 0), min_scroll_items)
            scroll_y_users = max(min(scroll_y_users, 0), min_scroll_users)
            scroll_y_report = max(min(scroll_y_report, 0), min_scroll_report)

            # Cadastro de usuário
            if state == "add_user":
                for box in user_boxes:
                    result = box.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    nome = user_boxes[0].get_text()
                    tipo = user_boxes[1].get_text().lower()
                    if nome and tipo:
                        if tipo == "aluno":
                            add_user(Student(next_user_id, nome))
                        elif tipo == "professor":
                            add_user(Professor(next_user_id, nome))
                        elif tipo == "visitante":
                            add_user(Visitor(next_user_id, nome))
                        next_user_id += 1
                        user_boxes[0].text = ""
                        user_boxes[1].text = ""
            # Cadastro de item
            elif state == "add_item":
                for box in item_boxes:
                    result = box.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    nome = item_boxes[0].get_text()
                    tipo = item_boxes[1].get_text().lower()
                    info = item_boxes[2].get_text()
                    autores = item_boxes[3].get_text().split(",") if item_boxes[3].get_text() else []
                    if nome and tipo:
                        if tipo == "livro":
                            add_item(Book(next_item_id, nome, info, autores))
                        elif tipo == "revista":
                            add_item(Magazine(next_item_id, nome, info))
                        elif tipo == "dvd":
                            try:
                                duracao = int(info)
                            except:
                                duracao = 0
                            add_item(DVD(next_item_id, nome, duracao))
                        next_item_id += 1
                        for box in item_boxes:
                            box.text = ""
            # Remover usuário
            elif state == "remove_user":
                result = remove_user_box.handle_event(event)
                if result is not None:
                    try:
                        uid = int(remove_user_box.get_text())
                        remove_user(uid)
                    except:
                        pass
                    remove_user_box.text = ""
            # Remover item
            elif state == "remove_item":
                result = remove_item_box.handle_event(event)
                if result is not None:
                    try:
                        iid = int(remove_item_box.get_text())
                        remove_item(iid)
                    except:
                        pass
                    remove_item_box.text = ""
            # Empréstimo
            elif state == "loan":
                for box in loan_boxes:
                    result = box.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    try:
                        uid = int(loan_boxes[0].get_text())
                        iid = int(loan_boxes[1].get_text())
                        user = next((u for u in users if u.id == uid), None)
                        item = next((i for i in items if i.id == iid and i.available), None)
                        if user and item:
                            if process_loan(user, item):
                                print(f"Usuário {user.id} ({user.name}) emprestou o item {item.id} ({item.name})")
                    except:
                        pass
                    loan_boxes[0].text = ""
                    loan_boxes[1].text = ""
            # Devolução
            elif state == "return":
                for box in return_boxes:
                    result = box.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    try:
                        uid = int(return_boxes[0].get_text())
                        iid = int(return_boxes[1].get_text())
                        user = next((u for u in users if u.id == uid), None)
                        item = next((i for i in items if i.id == iid and not i.available), None)
                        if user and item:
                            process_return(user, item)
                            print(f"Usuário {user.id} ({user.name}) devolveu o item {item.id} ({item.name})")
                    except:
                        pass
                    return_boxes[0].text = ""
                    return_boxes[1].text = ""

            # Navegação
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if state == "menu":
                    if 60 <= mx <= 380:
                        if 100 <= my <= 160: state = "add_item"
                        elif 180 <= my <= 240: state = "remove_item"
                        elif 260 <= my <= 320: state = "add_user"
                        elif 340 <= my <= 400: state = "remove_user"
                        elif 420 <= my <= 480: state = "loan"
                        elif 500 <= my <= 560: state = "return"
                        elif 580 <= my <= 640: state = "report"
                        elif 660 <= my <= 720: state = "stats"
                    if 800 <= mx <= 1120 and 700 <= my <= 760: pygame.quit(); return
                else:
                    if 10 <= mx <= 110 and 10 <= my <= 50:
                        state = "menu"

        # Botão de voltar
        if state != "menu":
            draw_button(screen, "< Voltar", 10, 10, 100, 40, GRAY, font)

        if state == "menu":
            main_menu(screen, font)
            item_shelf(screen, font, scroll_y=scroll_y_items)
        elif state == "add_item":
            draw_button(screen, "Preencha os campos e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            for box in item_boxes:
                box.draw(screen)
            item_shelf(screen, font, start_y=520, scroll_y=scroll_y_items)
        elif state == "remove_item":
            draw_button(screen, "Digite o ID do item para remover e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            remove_item_box.draw(screen)
            item_shelf(screen, font, start_y=280, scroll_y=scroll_y_items)
        elif state == "add_user":
            draw_button(screen, "Preencha os campos e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            for box in user_boxes:
                box.draw(screen)
            user_list(screen, font, start_y=380, scroll_y=scroll_y_users)
        elif state == "remove_user":
            draw_button(screen, "Digite o ID do usuário para remover e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            remove_user_box.draw(screen)
            user_list(screen, font, start_y=280, scroll_y=scroll_y_users)
        elif state == "loan":
            draw_button(screen, "Digite o ID do usuário e do item disponível e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            for box in loan_boxes:
                box.draw(screen)
            available_items = [item for item in items if item.available]
            user_list_left(screen, font, start_y=380, scroll_y=scroll_y_users)
            item_shelf_right(screen, font, available_items, start_y=380, scroll_y=scroll_y_items)

        elif state == "return":
            draw_button(screen, "Digite o ID do usuário e do item emprestado e pressione ENTER", 200, 120, 600, 50, GRAY, font)
            for box in return_boxes:
                box.draw(screen)
            loaned_items = [item for item in items if not item.available]
            user_list_left(screen, font, start_y=380, scroll_y=scroll_y_users)
            item_shelf_right(screen, font, loaned_items, start_y=380, scroll_y=scroll_y_items)
        elif state == "report":
            draw_button(screen, "Relatório de Empréstimos", 60, 40, 400, 50, GRAY, font)
            loan_report(screen, font, start_y=100, scroll_y=scroll_y_report)
        elif state == "stats":
            stats_screen(screen, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()