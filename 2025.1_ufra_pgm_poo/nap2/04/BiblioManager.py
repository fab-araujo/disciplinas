import pygame
import json
import abc
import uuid
from datetime import datetime
from typing import Dict, List, Optional


DATA_FILE = "bibliomanager.json"

# -------------------------
# Abstrações e Entidades
# -------------------------
class LibraryEntity(abc.ABC):
    def __init__(self, id: str, name: str):
        self.__id = id
        self.__name = name
        self.__created = datetime.now().isoformat()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, v: str):
        if not v:
            raise ValueError("name não pode ser vazio")
        self.__name = v

    @property
    def created(self) -> str:
        return self.__created

    @abc.abstractmethod
    def display_info(self) -> str:
        pass

    @abc.abstractmethod
    def update_status(self, new_status: str):
        pass

    @abc.abstractmethod
    def validate(self) -> bool:
        pass

    @abc.abstractmethod
    def serialize(self) -> dict:
        pass


class Item(LibraryEntity):
    def __init__(self, id: str, name: str, status: str = "available"):
        super().__init__(id, name)
        self.__status = status

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, s: str):
        if s not in ("available", "borrowed", "reserved"):
            raise ValueError("status inválido")
        self.__status = s

    def update_status(self, new_status: str):
        self.status = new_status

    def validate(self) -> bool:
        return bool(self.name)

    def serialize(self) -> dict:
        return {"id": self.id, "name": self.name, "status": self.status, "type": self.__class__.__name__}


class Book(Item):
    def __init__(self, id: str, name: str, author: str, isbn: str, year: str, status: str = "available"):
        super().__init__(id, name, status)
        self.__author = author
        self.__isbn = isbn
        self.__year = year

    def display_info(self) -> str:
        return f"Livro: {self.name} | Autor: {self.__author} | ISBN: {self.__isbn} | {self.status}"

    def serialize(self) -> dict:
        d = super().serialize()
        d.update({"author": self.__author, "isbn": self.__isbn, "year": self.__year})
        return d

    @classmethod
    def deserialize(cls, d: dict):
        return cls(d["id"], d["name"], d.get("author", ""), d.get("isbn", ""), d.get("year", ""), d.get("status", "available"))


class Magazine(Item):
    def __init__(self, id: str, name: str, issue: str, status: str = "available"):
        super().__init__(id, name, status)
        self.__issue = issue

    def display_info(self) -> str:
        return f"Revista: {self.name} | Edição: {self.__issue} | {self.status}"

    def serialize(self) -> dict:
        d = super().serialize()
        d.update({"issue": self.__issue})
        return d

    @classmethod
    def deserialize(cls, d: dict):
        return cls(d["id"], d["name"], d.get("issue", ""), d.get("status", "available"))


class DVD(Item):
    def __init__(self, id: str, name: str, director: str, duration: str, status: str = "available"):
        super().__init__(id, name, status)
        self.__director = director
        self.__duration = duration

    def display_info(self) -> str:
        return f"DVD: {self.name} | Dir: {self.__director} | {self.__duration} min | {self.status}"

    def serialize(self) -> dict:
        d = super().serialize()
        d.update({"director": self.__director, "duration": self.__duration})
        return d

    @classmethod
    def deserialize(cls, d: dict):
        return cls(d["id"], d["name"], d.get("director", ""), d.get("duration", ""), d.get("status", "available"))


# -------------------------
# Usuários
# -------------------------
class User(LibraryEntity):
    def __init__(self, id: str, name: str, email: str, user_type: str):
        super().__init__(id, name)
        self.__email = email
        self.__user_type = user_type
        self.__borrowed: List[str] = []

    @property
    def email(self) -> str:
        return self.__email

    @property
    def user_type(self) -> str:
        return self.__user_type

    @property
    def borrowed(self) -> List[str]:
        return list(self.__borrowed)

    def _borrow_direct(self, item_id: str):
        self.__borrowed.append(item_id)

    def _return_direct(self, item_id: str):
        if item_id in self.__borrowed:
            self.__borrowed.remove(item_id)

    def update_status(self, new_status: str):
        pass

    def validate(self) -> bool:
        return bool(self.name and self.__email)

    def display_info(self) -> str:
        return f"{self.__user_type.capitalize()}: {self.name} | Itens: {len(self.__borrowed)}"

    def can_borrow(self) -> bool:
        if self.__user_type == "student" and len(self.__borrowed) >= 5:
            return False
        if self.__user_type == "visitor" and len(self.__borrowed) >= 2:
            return False
        return True

    def serialize(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.__email,
                "user_type": self.__user_type, "borrowed": self.__borrowed}


class Student(User):
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email, "student")


class Professor(User):
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email, "professor")


class Visitor(User):
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email, "visitor")


# -------------------------
# Transactions
# -------------------------
class Transaction:
    def __init__(self, tx_id: str, tx_type: str, user_id: str, item_id: str, when: Optional[str] = None):
        self.__id = tx_id
        self.__type = tx_type  
        self.__user_id = user_id
        self.__item_id = item_id
        self.__when = when or datetime.now().isoformat()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def tx_type(self) -> str:
        return self.__type

    @property
    def user_id(self) -> str:
        return self.__user_id

    @property
    def item_id(self) -> str:
        return self.__item_id

    @property
    def when(self) -> str:
        return self.__when

    def serialize(self) -> dict:
        return {"id": self.__id, "type": self.__type, "user_id": self.__user_id, "item_id": self.__item_id, "when": self.__when}

    @classmethod
    def deserialize(cls, d: dict):
        return cls(d["id"], d["type"], d["user_id"], d["item_id"], d.get("when"))


# -------------------------
# UI / Manager
# -------------------------
class BiblioManager:
    def __init__(self, width: int = 1024, height: int = 768):
        pygame.init()
        pygame.font.init()
        self.W, self.H = width, height
        self.screen = pygame.display.set_mode((self.W, self.H))
        pygame.display.set_caption("BiblioManager")
        self.FONT_SMALL = pygame.font.SysFont("Arial", 14)
        self.FONT_MED = pygame.font.SysFont("Arial", 20)
        self.FONT_LARGE = pygame.font.SysFont("Arial", 28)
        self.FONT_TITLE = pygame.font.SysFont("Arial", 38, bold=True)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (240, 240, 240)
        self.DARK_GRAY = (90, 90, 90)
        self.GREEN = (0, 170, 0)
        self.RED = (190, 20, 20)
        self.BLUE = (20, 60, 200)

        self.items: Dict[str, Item] = {}
        self.users: Dict[str, User] = {}
        self.transactions: List[Transaction] = []

        self.form_data: Dict[str, str] = {}
        self.active_input: Optional[str] = None
        self.input_text: str = ""
        self.current: str = "main"
        self.selected_user: Optional[str] = None
        self.selected_item: Optional[str] = None
        self.report_filter: str = "all"  

        self.load()

    # -------------------------
    # Persistence
    # -------------------------
    def gen_id(self) -> str:
        return str(uuid.uuid4())

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            payload = {
                "items": {k: v.serialize() for k, v in self.items.items()},
                "users": {k: v.serialize() for k, v in self.users.items()},
                "transactions": [t.serialize() for t in self.transactions]
            }
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load(self):
        try:
            with open(DATA_FILE, encoding="utf-8") as f:
                d = json.load(f)
        except FileNotFoundError:
            return
        for k, v in d.get("items", {}).items():
            t = v.get("type")
            if t == "Book":
                self.items[k] = Book.deserialize(v)
            elif t == "Magazine":
                self.items[k] = Magazine.deserialize(v)
            elif t == "DVD":
                self.items[k] = DVD.deserialize(v)
        for k, v in d.get("users", {}).items():
            typ = v.get("user_type", "visitor")
            if typ == "student":
                u = Student(v["id"], v["name"], v.get("email", ""))
            elif typ == "professor":
                u = Professor(v["id"], v["name"], v.get("email", ""))
            else:
                u = Visitor(v["id"], v["name"], v.get("email", ""))
            # restore borrowed list privately
            for bid in v.get("borrowed", []):
                u._User__borrowed = v.get("borrowed", []) 
            self.users[k] = u
        for tx in d.get("transactions", []):
            self.transactions.append(Transaction.deserialize(tx))

    # -------------------------
    # UI Helpers
    # -------------------------
    def draw_text(self, text: str, font, x: int, y: int):
        self.screen.blit(font.render(text, True, self.BLACK), (x, y))

    def draw_button(self, rect: pygame.Rect, text: str, color=None):
        if color is None:
            color = self.GRAY
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)
        self.screen.blit(self.FONT_MED.render(text, True, self.BLACK), (rect.x + 10, rect.y + 8))

    def text_input_field(self, label: str, key: str, y: int) -> pygame.Rect:
        self.draw_text(label, self.FONT_MED, 60, y)
        r = pygame.Rect(300, y, 400, 30)
        val = self.form_data.get(key, "")
        pygame.draw.rect(self.screen, self.WHITE, r)
        pygame.draw.rect(self.screen, self.BLACK, r, 1)
        text = self.input_text if self.active_input == key else val
        self.screen.blit(self.FONT_MED.render(text, True, self.BLACK), (r.x + 6, r.y + 4))
        return r

    # -------------------------
    # Telas
    # -------------------------
    def draw_main(self):
        self.screen.fill(self.WHITE)
        title = self.FONT_TITLE.render("BiblioManager", True, self.BLUE)
        self.screen.blit(title, (380, 50))
        buttons = [("Itens", "items", 200), ("Usuários", "users", 280),
                   ("Listar Itens", "list_items", 360), ("Empréstimos", "loans", 440),
                   ("Relatórios", "reports", 520), ("Sair", "exit", 600)]
        for text, act, y in buttons:
            r = pygame.Rect(360, y, 300, 50)
            self.draw_button(r, text)
            if r.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.current = act
                pygame.time.delay(150)

    def draw_items_menu(self):
        self.screen.fill(self.WHITE)
        t = self.FONT_LARGE.render("Gerenciar Itens", True, self.BLUE)
        self.screen.blit(t, (340, 80))
        opts = [("Adicionar Livro", "add_book", 200),
                ("Adicionar Revista", "add_mag", 280),
                ("Adicionar DVD", "add_dvd", 360),
                ("Voltar", "main", 440)]
        for text, act, y in opts:
            r = pygame.Rect(360, y, 300, 50)
            self.draw_button(r, text)
            if r.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.current = act
                pygame.time.delay(150)

    def draw_list_items(self):
        self.screen.fill(self.WHITE)
        t = self.FONT_LARGE.render("Itens Cadastrados", True, self.BLUE)
        self.screen.blit(t, (320, 60))
        y = 120
        for it in self.items.values():
            self.screen.blit(self.FONT_SMALL.render(it.display_info(), True, self.BLACK), (60, y))
            y += 30
            if y > 700: break
        back = pygame.Rect(360, 700, 300, 40)
        self.draw_button(back, "Voltar")
        if back.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.current = "main"
            pygame.time.delay(150)

    def draw_add_book(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Adicionar Livro", True, self.BLUE), (340, 60))
        r1 = self.text_input_field("Nome:", "book_name", 150)
        r2 = self.text_input_field("Autor:", "book_author", 200)
        r3 = self.text_input_field("ISBN:", "book_isbn", 250)
        r4 = self.text_input_field("Ano:", "book_year", 300)
        save = pygame.Rect(360, 400, 120, 40)
        back = pygame.Rect(520, 400, 120, 40)
        self.draw_button(save, "Salvar", self.GREEN)
        self.draw_button(back, "Voltar", self.RED)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if save.collidepoint((mx, my)):
                name = self.form_data.get("book_name", "").strip()
                author = self.form_data.get("book_author", "").strip()
                isbn = self.form_data.get("book_isbn", "").strip()
                year = self.form_data.get("book_year", "").strip()
                if name and author:
                    b = Book(self.gen_id(), name, author, isbn, year)
                    self.items[b.id] = b
                    self.save()
                    self.form_data.clear()
                self.current = "items"
                pygame.time.delay(150)
            elif back.collidepoint((mx, my)):
                self.current = "items"
                pygame.time.delay(150)
            elif r1.collidepoint((mx, my)):
                self.switch_field("book_name")
            elif r2.collidepoint((mx, my)):
                self.switch_field("book_author")
            elif r3.collidepoint((mx, my)):
                self.switch_field("book_isbn")
            elif r4.collidepoint((mx, my)):
                self.switch_field("book_year")

    def draw_add_mag(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Adicionar Revista", True, self.BLUE), (340, 60))
        r1 = self.text_input_field("Nome:", "mag_name", 150)
        r2 = self.text_input_field("Edição:", "mag_issue", 200)
        save = pygame.Rect(360, 300, 120, 40)
        back = pygame.Rect(520, 300, 120, 40)
        self.draw_button(save, "Salvar", self.GREEN)
        self.draw_button(back, "Voltar", self.RED)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if save.collidepoint((mx, my)):
                name = self.form_data.get("mag_name", "").strip()
                issue = self.form_data.get("mag_issue", "").strip()
                if name and issue:
                    m = Magazine(self.gen_id(), name, issue)
                    self.items[m.id] = m
                    self.save()
                    self.form_data.clear()
                self.current = "items"
                pygame.time.delay(150)
            elif back.collidepoint((mx, my)):
                self.current = "items"
                pygame.time.delay(150)
            elif r1.collidepoint((mx, my)):
                self.switch_field("mag_name")
            elif r2.collidepoint((mx, my)):
                self.switch_field("mag_issue")

    def draw_add_dvd(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Adicionar DVD", True, self.BLUE), (340, 60))
        r1 = self.text_input_field("Nome:", "dvd_name", 150)
        r2 = self.text_input_field("Diretor:", "dvd_director", 200)
        r3 = self.text_input_field("Duração (min):", "dvd_duration", 250)
        save = pygame.Rect(360, 340, 120, 40)
        back = pygame.Rect(520, 340, 120, 40)
        self.draw_button(save, "Salvar", self.GREEN)
        self.draw_button(back, "Voltar", self.RED)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if save.collidepoint((mx, my)):
                name = self.form_data.get("dvd_name", "").strip()
                director = self.form_data.get("dvd_director", "").strip()
                duration = self.form_data.get("dvd_duration", "").strip()
                if name and director:
                    d = DVD(self.gen_id(), name, director, duration)
                    self.items[d.id] = d
                    self.save()
                    self.form_data.clear()
                self.current = "items"
                pygame.time.delay(150)
            elif back.collidepoint((mx, my)):
                self.current = "items"
                pygame.time.delay(150)
            elif r1.collidepoint((mx, my)):
                self.switch_field("dvd_name")
            elif r2.collidepoint((mx, my)):
                self.switch_field("dvd_director")
            elif r3.collidepoint((mx, my)):
                self.switch_field("dvd_duration")

    def draw_users(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Cadastrar Novo Usuário", True, self.BLUE), (300, 60))
    
    # Botões para escolher tipo de usuário
        btn_student = pygame.Rect(300, 120, 120, 40)
        btn_prof = pygame.Rect(440, 120, 120, 40)
        btn_visit = pygame.Rect(580, 120, 120, 40)
        self.draw_button(btn_student, "Aluno")
        self.draw_button(btn_prof, "Professor")
        self.draw_button(btn_visit, "Visitante")
    
        # Tipo selecionado
        utype = self.form_data.get("user_type", "student")
        self.draw_text(f"Selecionado: {utype.capitalize()}", self.FONT_MED, 300, 170)
    
        # Campos comuns
        r_name = self.text_input_field("Nome:", "user_name", 200)
        r_email = self.text_input_field("Email:", "user_email", 250)

        # Campos específicos
        if utype == "student":
            r_number = self.text_input_field("Número de Matrícula:", "user_number", 300)
        elif utype == "professor":
            r_dept = self.text_input_field("Departamento:", "user_department", 300)

        # Botões Salvar e Voltar
        save = pygame.Rect(300, 360, 120, 40)
        back = pygame.Rect(460, 360, 120, 40)
        self.draw_button(save, "Salvar", self.GREEN)
        self.draw_button(back, "Voltar", self.RED)

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            # Seleção de tipo
            if btn_student.collidepoint((mx, my)):
                self.form_data["user_type"] = "student"
                pygame.time.delay(120)
            elif btn_prof.collidepoint((mx, my)):
                self.form_data["user_type"] = "professor"
                pygame.time.delay(120)
            elif btn_visit.collidepoint((mx, my)):
                self.form_data["user_type"] = "visitor"
                pygame.time.delay(120)
            # Salvar usuário
            elif save.collidepoint((mx, my)):
                name = self.form_data.get("user_name", "").strip()
                email = self.form_data.get("user_email", "").strip()
                utype = self.form_data.get("user_type", "student")
                if name and email:
                    if utype == "student":
                        number = self.form_data.get("user_number", "").strip()
                        u = Student(self.gen_id(), name, email)
                        u.number = number  # Armazena matrícula
                    elif utype == "professor":
                        dept = self.form_data.get("user_department", "").strip()
                        u = Professor(self.gen_id(), name, email)
                        u.department = dept  # Armazena departamento
                    else:
                        u = Visitor(self.gen_id(), name, email)
                    self.users[u.id] = u
                    self.save()
                    self.form_data.clear()
                self.current = "main"
                pygame.time.delay(150)
        # Voltar
            elif back.collidepoint((mx, my)):
                self.current = "main"
                pygame.time.delay(150)
        # Clique nos campos
            elif r_name.collidepoint((mx, my)):
                self.switch_field("user_name")
            elif r_email.collidepoint((mx, my)):
                self.switch_field("user_email")
            elif utype == "student" and r_number.collidepoint((mx, my)):
                self.switch_field("user_number")
            elif utype == "professor" and r_dept.collidepoint((mx, my)):
                self.switch_field("user_department")


    def draw_loans(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Gerenciar Empréstimos", True, self.BLUE), (320, 40))
        y = 100
        self.draw_text("Usuários:", self.FONT_MED, 60, y)
        y += 30
        for u in list(self.users.values()):
            rect = pygame.Rect(60, y, 400, 30)
            pygame.draw.rect(self.screen, self.LIGHT_GRAY if self.selected_user == u.id else self.WHITE, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 1)
            self.screen.blit(self.FONT_SMALL.render(u.display_info(), True, self.BLACK), (rect.x + 5, rect.y + 5))
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.selected_user = u.id
                pygame.time.delay(120)
            y += 35
            if y > 300: break
        y = 360
        self.draw_text("Itens:", self.FONT_MED, 60, y)
        y += 30
        for it in list(self.items.values()):
            rect = pygame.Rect(60, y, 400, 30)
            pygame.draw.rect(self.screen, self.LIGHT_GRAY if self.selected_item == it.id else self.WHITE, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 1)
            self.screen.blit(self.FONT_SMALL.render(it.display_info(), True, self.BLACK), (rect.x + 5, rect.y + 5))
            if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.selected_item = it.id
                pygame.time.delay(120)
            y += 35
            if y > 600: break
        loan_btn = pygame.Rect(500, 600, 150, 40)
        return_btn = pygame.Rect(680, 600, 150, 40)
        back = pygame.Rect(360, 680, 300, 40)
        self.draw_button(loan_btn, "Emprestar", self.GREEN)
        self.draw_button(return_btn, "Devolver", self.BLUE)
        self.draw_button(back, "Voltar", self.RED)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if back.collidepoint((mx, my)):
                self.current = "main"
                pygame.time.delay(120)
            elif loan_btn.collidepoint((mx, my)):
                self.do_loan()
                pygame.time.delay(120)
            elif return_btn.collidepoint((mx, my)):
                self.do_return()
                pygame.time.delay(120)

    def draw_reports(self):
        self.screen.fill(self.WHITE)
        self.screen.blit(self.FONT_LARGE.render("Relatórios", True, self.BLUE), (320, 40))
        # Filter buttons
        all_btn = pygame.Rect(60, 100, 120, 40)
        loan_btn = pygame.Rect(200, 100, 120, 40)
        return_btn = pygame.Rect(340, 100, 120, 40)
        res_btn = pygame.Rect(480, 100, 160, 40)
        self.draw_button(all_btn, "Todas")
        self.draw_button(loan_btn, "Empréstimos")
        self.draw_button(return_btn, "Devoluções")
        self.draw_button(res_btn, "Reservas")
        self.draw_text(f"Filtro: {self.report_filter}", self.FONT_MED, 660, 110)
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if all_btn.collidepoint((mx, my)):
                self.report_filter = "all"
                pygame.time.delay(120)
            elif loan_btn.collidepoint((mx, my)):
                self.report_filter = "loan"
                pygame.time.delay(120)
            elif return_btn.collidepoint((mx, my)):
                self.report_filter = "return"
                pygame.time.delay(120)
            elif res_btn.collidepoint((mx, my)):
                self.report_filter = "reservation"
                pygame.time.delay(120)
        y = 160
        for tx in reversed(self.transactions): 
            if self.report_filter != "all" and tx.tx_type != self.report_filter:
                continue
            user = self.users.get(tx.user_id)
            item = self.items.get(tx.item_id)
            text = f"[{tx.when.split('T')[0]}] {tx.tx_type.capitalize()} - User: {user.name if user else tx.user_id} - Item: {item.name if item else tx.item_id}"
            self.screen.blit(self.FONT_SMALL.render(text, True, self.BLACK), (60, y))
            y += 24
            if y > 700: break
        back = pygame.Rect(360, 700, 300, 40)
        self.draw_button(back, "Voltar")
        if back.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.current = "main"
            pygame.time.delay(120)

    # -------------------------
    # Regras de negócio
    # -------------------------
    def do_loan(self):
        if not self.selected_user or not self.selected_item:
            return
        u = self.users.get(self.selected_user)
        it = self.items.get(self.selected_item)
        if not u or not it:
            return
        if it.status != "available":
            return
        if not u.can_borrow():
            return

        u._borrow_direct(it.id) 
        it.update_status("borrowed")
        tx = Transaction(self.gen_id(), "loan", u.id, it.id)
        self.transactions.append(tx)
        self.save()

    def do_return(self):
        if not self.selected_user or not self.selected_item:
            return
        u = self.users.get(self.selected_user)
        it = self.items.get(self.selected_item)
        if not u or not it:
            return
        if it.id not in u.borrowed:
            return
        u._return_direct(it.id)  
        it.update_status("available")
        tx = Transaction(self.gen_id(), "return", u.id, it.id)
        self.transactions.append(tx)
        self.save()

    # -------------------------
    # Auxiliar
    # -------------------------
    def switch_field(self, key: str):
        if self.active_input:
            self.form_data[self.active_input] = self.input_text
        self.active_input = key
        self.input_text = self.form_data.get(key, "")

    # -------------------------
    # Loop principal
    # -------------------------
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and self.active_input:
                    if e.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif e.key == pygame.K_RETURN:
                        self.form_data[self.active_input] = self.input_text
                        self.active_input = None
                        self.input_text = ""
                    else:
                        self.input_text += e.unicode

            if self.current == "main":
                self.draw_main()
            elif self.current == "items":
                self.draw_items_menu()
            elif self.current == "list_items":
                self.draw_list_items()
            elif self.current == "add_book":
                self.draw_add_book()
            elif self.current == "add_mag":
                self.draw_add_mag()
            elif self.current == "add_dvd":
                self.draw_add_dvd()
            elif self.current == "users":
                self.draw_users()
            elif self.current == "loans":
                self.draw_loans()
            elif self.current == "reports":
                self.draw_reports()
            elif self.current == "exit":
                running = False

            pygame.display.flip()
            clock.tick(30)
        self.save()
        pygame.quit()


if __name__ == "__main__":
    BiblioManager().run()
