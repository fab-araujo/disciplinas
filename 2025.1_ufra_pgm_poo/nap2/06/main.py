import pygame
import json
from abc import ABC, abstractmethod
import datetime
import time

pygame.init()

# ------------------- Configurações da tela -------------------
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BiblioManager")
FONT = pygame.font.SysFont("Verdana", 20)
SMALL_FONT = pygame.font.SysFont("Verdana", 16)
TITLE_FONT = pygame.font.SysFont("Verdana", 28, bold=True)

# Cores
WHITE = (216,216,191)
GRAY = (220, 220, 220)
DARKGRAY = (64, 61, 61)
GREEN = (79, 168, 130)
RED = (224, 102, 54)
BLUE = (0,0,0)
ORANGE = (220, 220, 220)
PURPLE = (35,107,142)
BLACK = (0, 0, 0)

# ------------------- Funções JSON -------------------
def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ------------------- Classes -------------------
class LibraryEntity(ABC):
    def __init__(self, id_):
        self.__id = id_

    @abstractmethod
    def display_info(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @property
    def id(self):
        return self.__id

class Item(LibraryEntity):
    def __init__(self, id_, name):
        super().__init__(id_)
        self.name = name
        self.status = "Disponível"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }

class Book(Item):
    def __init__(self, id_, name, author, publisher, year, isbn):
        super().__init__(id_, name)
        self.author = author
        self.publisher = publisher
        self.year = year
        self.isbn = isbn

    def display_info(self):
        return f"{self.name} | {self.author} | {self.publisher} | {self.year} | {self.isbn} | {self.status}"

    def serialize(self):
        data = super().serialize()
        data.update({
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "isbn": self.isbn,
            "type": "Book"
        })
        return data

class User(LibraryEntity):
    def __init__(self, id_, matricula, name):
        super().__init__(id_)
        self.matricula = matricula
        self.name = name
        

    @abstractmethod
    def display_info(self):
        pass

    def serialize(self):
        return {
            "id": self.id,
            "matricula": self.matricula,
            "name": self.name,
            "type": self.__class__.__name__
        }

class Student(User):
    MAX_LOANS = 5
    def display_info(self):
        return f"{self.matricula} | {self.name} | Aluno"

class Professor(User):
    def display_info(self):
        return f"{self.matricula} | {self.name} | Professor"

# ------------------- Transações -------------------
class Transaction(ABC):
    @abstractmethod
    def process(self, user, item):
        pass

class Loan(Transaction):
    def process(self, user, item):
        loans = load_json("emprestimos.json")
        user_loans = [l for l in loans if l["user_id"] == user.id and l["return_date"] is None]
        if isinstance(user, Student) and len(user_loans) >= Student.MAX_LOANS:
            return False, "Aluno atingiu limite de empréstimos"
        if item.status != "Disponível":
            return False, "Livro não disponível"
        item.status = "Emprestado"
        loans.append({
            "user_id": user.id,
            "item_id": item.id,
            "date": str(datetime.date.today()),
            "return_date": None
        })
        save_json("emprestimos.json", loans)
        return True, "Empréstimo realizado"

class Return(Transaction):
    def process(self, user, item):
        loans = load_json("emprestimos.json")
        for loan in loans:
            if loan["user_id"] == user.id and loan["item_id"] == item.id and loan["return_date"] is None:
                loan["return_date"] = str(datetime.date.today())
                save_json("emprestimos.json", loans)
                item.status = "Disponível"
                return True, "Livro devolvido"
        return False, "Nenhum empréstimo encontrado"

# ------------------- Interface -------------------
class Button:
    def __init__(self, x, y, w, h, text, base_color=PURPLE, hover_color=ORANGE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.current_color = base_color
        self.txt_surface = FONT.render(text, True, BLACK)

    def draw(self, win):
        self.current_color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.base_color
        pygame.draw.rect(win, self.current_color, self.rect, border_radius=10)
        win.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class InputBox:
    def __init__(self, x, y, w, h, placeholder=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = GRAY
        self.color_active = BLUE
        self.color = self.color_inactive
        self.text = ''
        self.placeholder = placeholder
        self.txt_surface = FONT.render(placeholder, True, DARKGRAY)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                text = self.text
                self.text = ''
                self.txt_surface = FONT.render(self.placeholder, True, DARKGRAY)
                return text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text if self.text else self.placeholder, True, BLACK)
        return None

    def draw(self, win):
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(win, self.color, self.rect, 2, border_radius=5)

# ------------------- CRUD -------------------
def load_users():
    data = load_json("usuarios.json")
    users = []
    for d in data:
        matricula = d.get("matricula","00000")
        name = d.get("name","Sem Nome")
        if d["type"]=="Student":
            users.append(Student(d["id"], matricula, name))
        elif d["type"]=="Professor":
            users.append(Professor(d["id"], matricula, name))
    return users

def save_user(user):
    users = load_json("usuarios.json")
    users.append(user.serialize())
    save_json("usuarios.json", users)

def load_books():
    data = load_json("livros.json")
    books = []
    for d in data:
        if d.get("type")=="Book":
            book = Book(d["id"], d["name"], d["author"], d["publisher"], d["year"], d["isbn"])
            book.status = d.get("status","Disponível")
            books.append(book)
    return books

def save_book(book, limit=100):
    books = load_books()
    if len(books) >= limit:
        return False, f"Limite de {limit} livros atingido"
    data = load_json("livros.json")
    data.append(book.serialize())
    save_json("livros.json", data)
    return True, "Livro cadastrado"

# ------------------- Main -------------------
def main():
    clock = pygame.time.Clock()
    run = True

    # Botões do menu
    buttons = [
        Button(40,100,180,50,"Novo Usuário"),
        Button(40,170,180,50,"Novo Livro"),
        Button(40,240,180,50,"Ver Usuários"),
        Button(40,310,180,50,"Ver Livros"),
        Button(40,380,180,50,"Emprestar Livro"),
        Button(40,450,180,50,"Devolver Livro")
    ]

    active_screen = "home"
    input_boxes = []
    messages = []
    users = load_users()
    books = load_books()
    selected_type = 0
    user_types = ["Aluno","Professor"]

    # caixas cadastro separadas
    user_inputs = [
        InputBox(390,160,180, 35,"Matrícula"),
        InputBox(390,230,180, 35,"Nome"),
    ]
    book_inputs = [
        InputBox(390,160,180,35,"Nome do livro"),
        InputBox(390,230,180,35,"Autor"),
        InputBox(390,300,180,35,"Editora"),
        InputBox(390,370,180,35,"Ano"),
        InputBox(390,440,180,35,"ISBN")
    ]

    search_box = InputBox(600,120,200,35,"Pesquisar livro...")
    user_box = InputBox(300,120,250,35,"Matrícula do usuário")
    filtered_books = books.copy()
    selected_book = None
    save_button = Button(600,190,100,50,"Salvar", base_color=GREEN, hover_color=BLUE)
    emprestar_btn = Button(400,500,130,50,"Emprestar", base_color=GREEN, hover_color=BLUE)
    devolver_btn = Button(400,500,100,50,"Devolver", base_color=GREEN, hover_color=BLUE)

    screen_titles = {
        "home":"Tela Inicial",
        "novo_usuario":"Inserir Usuário",
        "novo_livro":"Inserir Livro",
        "ver_usuarios":"Visualizar Usuários",
        "ver_livros":"Visualizar Livros",
        "emprestar":"Emprestar Livro",
        "devolver":"Devolver Livro"
    }

    while run:
        WIN.fill(WHITE)
        title_text = TITLE_FONT.render(screen_titles.get(active_screen,"BiblioManager"), True, BLUE)
        WIN.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))

        for b in buttons:
            b.draw(WIN)

        if active_screen in ["novo_usuario","novo_livro"]:
            save_button.draw(WIN)

        y_msg = HEIGHT - 100
        current_time = time.time()
        messages = [(txt,color,timestamp) for txt,color,timestamp in messages if current_time-timestamp<3]
        for msg, color, _ in messages:
            txt_surface = SMALL_FONT.render(msg, True, color)
            WIN.blit(txt_surface, (220, y_msg))
            y_msg += 25

        # Desenha input boxes apenas nas telas de cadastro
        for box in input_boxes:
            box.draw(WIN)

        # Caixas específicas apenas para empréstimo/devolução
        if active_screen=="emprestar":
            search_box.draw(WIN)
            user_box.draw(WIN)
            emprestar_btn.draw(WIN)
        elif active_screen == "devolver":
        # Desenha input do usuário e botão
            user_box.draw(WIN)
            devolver_btn.draw(WIN)

            # Pega usuário digitado
            matricula = user_box.text
            user = next((u for u in users if u.matricula == matricula), None)
            
            if user:
                # Filtra livros emprestados pelo usuário
                user_loans = [
                    b for b in books 
                    if any(
                        l["item_id"] == b.id and l["user_id"] == user.id and l["return_date"] is None
                        for l in load_json("emprestimos.json")
                    )
                ]

                # Desenha livros na tela
                y_start = 180
                for b in user_loans:
                    pygame.draw.rect(WIN, GRAY, (300, y_start, 500, 30))
                    txt = SMALL_FONT.render(b.display_info(), True, BLACK)
                    WIN.blit(txt, (320, y_start + 5))
                    y_start += 35

        # Eventos
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            # Input boxes
            for box in input_boxes + ([search_box, user_box] if active_screen in ["emprestar","devolver"] else []):
                box.handle_event(event)

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                for i,b in enumerate(buttons):
                    if b.is_clicked(pos):
                        filtered_books = books.copy()
                        selected_book = None
                        user_box.text=""
                        search_box.text=""
                        # Define telas
                        if i==0:
                            input_boxes = user_inputs.copy()
                            active_screen="novo_usuario"
                        elif i==1:
                            input_boxes = book_inputs.copy()
                            active_screen="novo_livro"
                        elif i==2:
                            input_boxes=[]
                            active_screen="ver_usuarios"
                        elif i==3:
                            input_boxes=[]
                            active_screen="ver_livros"
                        elif i==4:
                            input_boxes=[]
                            active_screen="emprestar"
                        elif i==5:
                            input_boxes=[]
                            active_screen="devolver"

        # ---------------- Salvar usuário/livro ----------------
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if active_screen=="novo_usuario" and save_button.is_clicked(pos):
                if all(v.text for v in input_boxes):
                    id_ = len(users)+1
                    tipo = user_types[selected_type]
                    matricula=input_boxes[0].text
                    nome=input_boxes[1].text
                    new_user = Student(id_, matricula, nome) if tipo=="Aluno" else Professor(id_, matricula, nome)
                    users.append(new_user)
                    save_user(new_user)
                    messages.append(("Usuário cadastrado!", GREEN, time.time()))
                    for box in input_boxes:
                        box.text = ""
                        box.txt_surface = FONT.render(box.placeholder, True, DARKGRAY)
                else:
                    messages.append(("Preencha todos os campos!", RED, time.time()))
            if active_screen=="novo_livro" and save_button.is_clicked(pos):
                if all(v.text for v in input_boxes):
                    id_ = len(books)+1
                    nome=input_boxes[0].text
                    autor=input_boxes[1].text
                    editora=input_boxes[2].text
                    ano=input_boxes[3].text
                    isbn=input_boxes[4].text
                    new_book=Book(id_, nome, autor, editora, ano, isbn)
                    ok,msg=save_book(new_book)
                    messages.append((msg, GREEN if ok else RED, time.time()))
                    if ok:
                        books.append(new_book)
                        for box in input_boxes:
                            box.text= ""
                            box.txt_surface = FONT.render(box.placeholder, True, DARKGRAY)
                else:
                    messages.append(("Preencha todos os campos!", RED, time.time()))

        # ---------------- Emprestar livro ----------------
        if active_screen=="emprestar":
            filtered_books = [b for b in books if search_box.text.lower() in b.name.lower()]
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                y_start = 120
                for b in filtered_books:
                    rect = pygame.Rect(220, y_start, 550, 30)
                    if rect.collidepoint(pos):
                        selected_book = b
                    y_start += 35
                if emprestar_btn.is_clicked(pos):
                    matricula = user_box.text
                    user = next((u for u in users if u.matricula==matricula), None)
                    if not user:
                        messages.append(("Usuário não encontrado", RED, time.time()))
                    elif not selected_book:
                        messages.append(("Selecione um livro", RED, time.time()))
                    else:
                        ok,msg = Loan().process(user, selected_book)
                        messages.append((msg, GREEN if ok else RED, time.time()))
                        selected_book = None

        # ---------------- Devolver livro ----------------
        if active_screen=="devolver":
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if devolver_btn.is_clicked(pos):
                    matricula = user_box.text
                    user = next((u for u in users if u.matricula==matricula), None)
                    if not user:
                        messages.append(("Usuário não encontrado", RED, time.time()))
                    else:
                        user_loans = [b for b in books if any(l["item_id"]==b.id and l["user_id"]==user.id and l["return_date"]==None for l in load_json("emprestimos.json"))]
                        if not user_loans:
                            messages.append(("Nenhum livro para devolver", RED, time.time()))
                        else:
                            for b in user_loans:
                                Return().process(user,b)
                            messages.append(("Livros devolvidos", GREEN, time.time()))

        # ---------------- Desenhar listas ----------------
        if active_screen=="ver_usuarios":
            y = 120
            for u in users:
                pygame.draw.rect(WIN, GRAY, (300,y,500,30))
                txt = SMALL_FONT.render(u.display_info(), True, BLACK)
                WIN.blit(txt, (320,y+5))
                y+=35
        elif active_screen=="ver_livros":
            y=120
            for b in books:
                pygame.draw.rect(WIN, GRAY, (300,y,500,30))
                txt = SMALL_FONT.render(b.display_info(), True, BLACK)
                WIN.blit(txt, (320,y+5))
                y+=35
        elif active_screen=="emprestar":
            y_start = 180
            for b in filtered_books:
                pygame.draw.rect(WIN, GRAY if b!=selected_book else ORANGE, (300,y_start,500,30))
                txt = SMALL_FONT.render(b.display_info(), True, BLACK)
                WIN.blit(txt, (320,y_start+5))
                y_start += 35

        pygame.display.update()
        clock.tick(60)

if __name__=="__main__":
    main()
