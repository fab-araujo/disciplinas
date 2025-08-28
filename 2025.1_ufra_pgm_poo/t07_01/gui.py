import pygame
from entities import Book, Magazine, Student, Professor, Loan, Return
import random

class LibraryGUI:
    def __init__(self, library):
        self.library = library
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("BiblioManager")
        self.clock = pygame.time.Clock()
        # Fonts (fallbacks ensured by pygame)
        self.font = pygame.font.SysFont("Segoe UI", 22) or pygame.font.SysFont("Arial", 22)
        self.title_font = pygame.font.SysFont("Segoe UI Semibold", 36) or pygame.font.SysFont("Arial", 36)
        self.state = "menu"
        self.input_text = ""
        self.selected_item = None
        self.selected_user = None
        self.buttons = []

        # Theme
        self.theme = {
            "text_primary": (30, 34, 39),
            "text_on_primary": (255, 255, 255),
            "muted": (90, 99, 110),
            "primary": (59, 130, 246),
            "success": (16, 185, 129),
            "danger": (239, 68, 68),
            "input_bg": (248, 250, 252),
            "input_border": (203, 213, 225)
        }

        # UI feedback
        self.toast_message = ""
        self.toast_until_ms = 0

    # Fundo sólido simples para legibilidade
    def clear_background(self):
        self.screen.fill((255, 255, 255))

    def draw_header(self, title):
        # Simplified: just draw the title text
        title_surface = self.title_font.render(title, True, (0, 0, 0))
        self.screen.blit(title_surface, (32, 20))

    def draw_button(self, rect, label, variant="primary", align_center_text=True):
        # Simplified button without hover/shadow
        if variant == "primary":
            color = self.theme["primary"]
        elif variant == "success":
            color = self.theme["success"]
        elif variant == "danger":
            color = self.theme["danger"]
        else:
            color = (148, 163, 184)
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        text_surface = self.font.render(label, True, self.theme["text_on_primary"])
        if align_center_text:
            text_pos = (rect.centerx - text_surface.get_width() // 2, rect.centery - text_surface.get_height() // 2)
        else:
            text_pos = (rect.x + 12, rect.y + (rect.h - text_surface.get_height()) // 2)
        self.screen.blit(text_surface, text_pos)

    def add_button(self, rect, action):
        self.buttons.append({"rect": rect, "action": action})

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.library.save_data()
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            self.clear_background()
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_click(self, pos):
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                button["action"]()

    def handle_key(self, event):
        if event.key == pygame.K_RETURN:
            if self.state == "add_item":
                self.add_item()
            elif self.state == "add_user":
                self.add_user()
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        elif event.unicode.isprintable():
            self.input_text += event.unicode

    def draw(self):
        self.buttons = []
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "items":
            self.draw_items()
        elif self.state == "users":
            self.draw_users()
        elif self.state == "add_item":
            self.draw_add_item()
        elif self.state == "edit_item":
            self.draw_edit_item()
        elif self.state == "add_user":
            self.draw_add_user()
        elif self.state == "edit_user":
            self.draw_edit_user()
        elif self.state == "transactions":
            self.draw_transactions()
        elif self.state == "report":
            self.draw_report()
        self.draw_toast()

    def show_toast(self, message, duration_ms=2000):
        self.toast_message = message
        self.toast_until_ms = pygame.time.get_ticks() + duration_ms

    def draw_toast(self):
        if not self.toast_message:
            return
        if pygame.time.get_ticks() > self.toast_until_ms:
            self.toast_message = ""
            return
        text_surface = self.font.render(self.toast_message, True, self.theme["text_on_primary"]) 
        padding_x, padding_y = 16, 10
        rect = pygame.Rect(0, 0, text_surface.get_width() + padding_x * 2, text_surface.get_height() + padding_y * 2)
        rect.centerx = 1024 // 2
        rect.y = 768 - rect.height - 24
        pygame.draw.rect(self.screen, (17, 24, 39), rect, border_radius=10)
        self.screen.blit(text_surface, (rect.x + padding_x, rect.y + padding_y))

    def draw_menu(self):
        self.draw_header("BiblioManager")
        buttons = [
            ("Items", lambda: setattr(self, "state", "items"), "primary"),
            ("Users", lambda: setattr(self, "state", "users"), "primary"),
            ("Transactions", lambda: setattr(self, "state", "transactions"), "primary"),
            ("Report", lambda: setattr(self, "state", "report"), "primary"),
            ("Exit", lambda: self.library.save_data() or pygame.quit(), "danger")
        ]
        for i, (text, action, variant) in enumerate(buttons):
            rect = pygame.Rect(312, 140 + i * 90, 400, 64)
            self.draw_button(rect, text, variant)
            self.add_button(rect, action)

    def draw_items(self):
        self.draw_header("Items")
        self.draw_back_button()
        button = pygame.Rect(312, 88, 400, 56)
        self.draw_button(button, "Add Item", "success")
        self.add_button(button, lambda: setattr(self, "state", "add_item"))
        for i, item in enumerate(self.library.get_items()):
            # Cada item ocupa dois "rows": 1) texto, 2) botões à direita
            base_y = 170 + i * 60
            text_surface = self.font.render(item.display_info(), True, self.theme["text_primary"])
            self.screen.blit(text_surface, (50, base_y))
            # Linha de botões (abaixo do texto), alinhados à direita
            btn_y = base_y + 24
            btn_w = 120
            btn_h = 32
            gap = 10
            right_margin = 50
            delete_x = 1024 - right_margin - btn_w
            select_x = delete_x - gap - btn_w
            rect = pygame.Rect(select_x, btn_y, btn_w, btn_h)
            self.draw_button(rect, "Select", "primary")
            def make_select_action(it):
                def _act():
                    self.selected_item = it
                    # Pre-fill edit text
                    # (display_info já é usado apenas para exibição)
                    # Build canonical edit string
                    if it.__class__.__name__.lower() == "book":
                        # Parse from serialize if available
                        info = it.serialize()
                        self.input_text = f"Book: {info.get('name','')}, {info.get('author','')}, {info.get('isbn','')}"
                    elif it.__class__.__name__.lower() == "magazine":
                        info = it.serialize()
                        self.input_text = f"Magazine: {info.get('name','')}, {info.get('edition','')}"
                    else:
                        self.input_text = ""
                    self.state = "edit_item"
                return _act
            self.add_button(rect, make_select_action(item))
            # Delete button (disabled if borrowed) na mesma linha, à direita
            del_rect = pygame.Rect(delete_x, btn_y, btn_w, btn_h)
            can_delete = getattr(item, 'status', 'available') == 'available'
            self.draw_button(del_rect, "Delete", "danger" if can_delete else "secondary")
            def make_delete_action(it):
                def _act():
                    try:
                        self.library.delete_item(it.id)
                        self.library.save_data()
                        self.show_toast("Item excluído.")
                    except Exception as e:
                        self.show_toast("Não é possível excluir: empréstimo em aberto.")
                return _act
            if can_delete:
                self.add_button(del_rect, make_delete_action(item))

    def draw_users(self):
        self.draw_header("Users")
        self.draw_back_button()
        button = pygame.Rect(312, 88, 400, 56)
        self.draw_button(button, "Add User", "success")
        self.add_button(button, lambda: setattr(self, "state", "add_user"))
        for i, user in enumerate(self.library.get_users()):
            # Dois "rows" por usuário: 1) texto, 2) botões à direita
            base_y = 170 + i * 60
            text_surface = self.font.render(user.display_info(), True, self.theme["text_primary"])
            self.screen.blit(text_surface, (50, base_y))
            btn_y = base_y + 24
            btn_w = 120
            btn_h = 32
            gap = 10
            right_margin = 50
            delete_x = 1024 - right_margin - btn_w
            select_x = delete_x - gap - btn_w
            rect = pygame.Rect(select_x, btn_y, btn_w, btn_h)
            self.draw_button(rect, "Select", "primary")
            def make_select_user_action(u):
                def _act():
                    self.selected_user = u
                    # Pre-fill edit string
                    # Determine type via display or serialize
                    info = u.serialize()
                    utype = info.get('user_type', 'student')
                    label = 'Student' if utype == 'student' else 'Professor'
                    self.input_text = f"{label}: {info.get('name','')}"
                    self.state = "edit_user"
                return _act
            self.add_button(rect, make_select_user_action(user))
            # Delete button (disabled if has borrowed items) à direita, na linha de baixo
            del_rect = pygame.Rect(delete_x, btn_y, btn_w, btn_h)
            can_delete = len(getattr(user, 'borrowed_items', [])) == 0
            self.draw_button(del_rect, "Delete", "danger" if can_delete else "secondary")
            def make_delete_user_action(u):
                def _act():
                    try:
                        self.library.delete_user(u.id)
                        self.library.save_data()
                        self.show_toast("Usuário excluído.")
                    except Exception:
                        self.show_toast("Não é possível excluir: empréstimo em aberto.")
                return _act
            if can_delete:
                self.add_button(del_rect, make_delete_user_action(user))

    def draw_edit_item(self):
        self.draw_header("Edit Item")
        self.draw_back_button()
        hint = "Edit and save (Book: Name, Author, ISBN) or (Magazine: Name, Edition):"
        hint_surface = self.font.render(hint, True, self.theme["muted"]) 
        self.screen.blit(hint_surface, (50, 100))
        input_rect = pygame.Rect(50, 150, 700, 44)
        pygame.draw.rect(self.screen, self.theme["input_bg"], input_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme["input_border"], input_rect, width=2, border_radius=8)
        text_surface = self.font.render(self.input_text, True, self.theme["text_primary"]) 
        self.screen.blit(text_surface, (input_rect.x + 12, input_rect.y + 10))
        save_rect = pygame.Rect(770, 150, 180, 44)
        self.draw_button(save_rect, "Save Changes", "primary")
        self.add_button(save_rect, self.save_edit_item)

    def draw_add_item(self):
        self.draw_header("Add Item")
        self.draw_back_button()
        hint = "Enter Item (e.g., 'Book: Name, Author, ISBN' or 'Magazine: Name, Edition'):"
        hint_surface = self.font.render(hint, True, self.theme["muted"]) 
        self.screen.blit(hint_surface, (50, 100))
        input_rect = pygame.Rect(50, 150, 700, 44)
        # input background and border
        pygame.draw.rect(self.screen, self.theme["input_bg"], input_rect, border_radius=8)
        border_color = self.theme["input_border"]
        pygame.draw.rect(self.screen, border_color, input_rect, width=2, border_radius=8)
        text_surface = self.font.render(self.input_text, True, self.theme["text_primary"]) 
        self.screen.blit(text_surface, (input_rect.x + 12, input_rect.y + 10))
        # Save button
        save_rect = pygame.Rect(770, 150, 180, 44)
        self.draw_button(save_rect, "Save Item", "primary")
        self.add_button(save_rect, self.add_item)

    def draw_add_user(self):
        self.draw_header("Add User")
        self.draw_back_button()
        hint = "Enter User (e.g., 'Student: Name' or 'Professor: Name'):"
        hint_surface = self.font.render(hint, True, self.theme["muted"]) 
        self.screen.blit(hint_surface, (50, 100))
        input_rect = pygame.Rect(50, 150, 700, 44)
        pygame.draw.rect(self.screen, self.theme["input_bg"], input_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme["input_border"], input_rect, width=2, border_radius=8)
        text_surface = self.font.render(self.input_text, True, self.theme["text_primary"]) 
        self.screen.blit(text_surface, (input_rect.x + 12, input_rect.y + 10))
        # Save button
        save_rect = pygame.Rect(770, 150, 180, 44)
        self.draw_button(save_rect, "Save User", "primary")
        self.add_button(save_rect, self.add_user)

    def draw_edit_user(self):
        self.draw_header("Edit User")
        self.draw_back_button()
        hint = "Edit and save (Student: Name) or (Professor: Name):"
        hint_surface = self.font.render(hint, True, self.theme["muted"]) 
        self.screen.blit(hint_surface, (50, 100))
        input_rect = pygame.Rect(50, 150, 700, 44)
        pygame.draw.rect(self.screen, self.theme["input_bg"], input_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.theme["input_border"], input_rect, width=2, border_radius=8)
        text_surface = self.font.render(self.input_text, True, self.theme["text_primary"]) 
        self.screen.blit(text_surface, (input_rect.x + 12, input_rect.y + 10))
        save_rect = pygame.Rect(770, 150, 180, 44)
        self.draw_button(save_rect, "Save Changes", "primary")
        self.add_button(save_rect, self.save_edit_user)

    def save_edit_item(self):
        if not self.selected_item:
            self.show_toast("Nenhum item selecionado.")
            return
        try:
            raw = self.input_text.strip()
            parts = raw.split(":", 1)
            if len(parts) < 2:
                self.show_toast("Formato inválido.")
                return
            type_, details_str = parts[0].strip().lower(), parts[1].strip()
            if type_ in ("livro",):
                type_ = "book"
            if type_ in ("revista",):
                type_ = "magazine"
            details = [d.strip() for d in details_str.split(",")]
            if type_ == "book" and len(details) == 3:
                new_data = {"type": "book", "name": details[0], "author": details[1], "isbn": details[2]}
            elif type_ == "magazine" and len(details) == 2:
                new_data = {"type": "magazine", "name": details[0], "edition": details[1]}
            else:
                self.show_toast("Dados insuficientes.")
                return
            self.library.update_item(self.selected_item.id, new_data)
            self.library.save_data()
            self.show_toast("Item atualizado com sucesso!")
            self.state = "items"
            self.input_text = ""
        except Exception as e:
            self.show_toast("Erro ao atualizar item.")

    def save_edit_user(self):
        if not self.selected_user:
            self.show_toast("Nenhum usuário selecionado.")
            return
        try:
            raw = self.input_text.strip()
            parts = raw.split(":", 1)
            if len(parts) < 2:
                self.show_toast("Formato inválido.")
                return
            type_, name = parts[0].strip().lower(), parts[1].strip()
            if type_ in ("aluno", "estudante", "usuario", "usuário", "user"):
                type_ = "student"
            if type_ == "professor":
                type_ = "professor"
            if not name:
                self.show_toast("Nome não pode ser vazio.")
                return
            self.library.update_user(self.selected_user.id, {"type": type_, "name": name})
            self.library.save_data()
            self.show_toast("Usuário atualizado com sucesso!")
            self.state = "users"
            self.input_text = ""
        except Exception as e:
            self.show_toast("Erro ao atualizar usuário.")

    def draw_transactions(self):
        self.draw_header("Transactions")
        self.draw_back_button()
        # Titles
        title_user = self.font.render("Select User", True, self.theme["muted"]) 
        self.screen.blit(title_user, (50, 90))

        # Users list (stacked)
        users = self.library.get_users()
        start_y = 120
        max_user_rows = 8
        user_rows = 0
        for i, u in enumerate(users[:max_user_rows]):
            y = start_y + i * 34
            btn = pygame.Rect(50, y - 4, 120, 28)
            self.draw_button(btn, "Select", "primary")
            info = self.font.render(u.display_info(), True, self.theme["text_primary"]) 
            self.screen.blit(info, (50 + 120 + 16, y))
            def make_sel_user(u_):
                def _act():
                    self.selected_user = u_
                    self.show_toast(f"User selecionado: {u_.name}")
                return _act
            self.add_button(btn, make_sel_user(u))
            user_rows += 1

        # Items title below users
        items_title_y = start_y + user_rows * 34 + 20
        title_item = self.font.render("Select Item (available)", True, self.theme["muted"]) 
        self.screen.blit(title_item, (50, items_title_y))

        # Items list (available only, stacked)
        items_start_y = items_title_y + 30
        items = [it for it in self.library.get_items() if getattr(it, 'status', 'available') == 'available']
        max_item_rows = 8
        item_rows = 0
        for i, it in enumerate(items[:max_item_rows]):
            y = items_start_y + i * 34
            btn = pygame.Rect(50, y - 4, 120, 28)
            self.draw_button(btn, "Select", "primary")
            info = self.font.render(it.display_info(), True, self.theme["text_primary"]) 
            self.screen.blit(info, (50 + 120 + 16, y))
            def make_sel_item(it_):
                def _act():
                    self.selected_item = it_
                    self.show_toast(f"Item selecionado: {it_.name}")
                return _act
            self.add_button(btn, make_sel_item(it))
            item_rows += 1

        # Current selection summary below items
        summary_y = items_start_y + item_rows * 34 + 20
        sel_summary = f"User: {self.selected_user.name if self.selected_user else '-'} | Item: {self.selected_item.name if self.selected_item else '-'}"
        sel_surface = self.font.render(sel_summary, True, self.theme["text_primary"]) 
        self.screen.blit(sel_surface, (50, summary_y))
        if self.selected_user and self.selected_item:
            button = pygame.Rect(50, summary_y + 32, 240, 44)
            self.draw_button(button, "Save Loan", "success")
            self.add_button(button, self.process_loan)
            clear_btn = pygame.Rect(300, summary_y + 32, 160, 44)
            self.draw_button(clear_btn, "Clear", "danger")
            self.add_button(clear_btn, lambda: (setattr(self, 'selected_user', None), setattr(self, 'selected_item', None)))

        # Open loans section below summary
        open_title_y = summary_y + 90
        open_title = self.font.render("Open Loans", True, self.theme["muted"]) 
        self.screen.blit(open_title, (50, open_title_y))
        row = 0
        for u in users:
            for it in getattr(u, 'borrowed_items', []):
                y = open_title_y + 30 + row * 26
                if y > 740:
                    break
                text = f"{u.name} — {it.name}"
                t_surf = self.font.render(text, True, self.theme["text_primary"]) 
                self.screen.blit(t_surf, (50, y))
                btn = pygame.Rect(420, y - 4, 180, 24)
                self.draw_button(btn, "Finalize", "primary")
                def make_finalize(u_, it_):
                    def _act():
                        self.process_return_for(u_, it_)
                    return _act
                self.add_button(btn, make_finalize(u, it))
                row += 1

    def draw_report(self):
        self.draw_header("Report")
        self.draw_back_button()
        report = self.library.generate_report().split("\n")
        for i, line in enumerate(report):
            text_surface = self.font.render(line, True, self.theme["text_primary"]) 
            self.screen.blit(text_surface, (50, 120 + i * 30))

    def draw_back_button(self):
        button = pygame.Rect(864, 8, 152, 48)
        self.draw_button(button, "Back", "danger")
        self.add_button(button, lambda: setattr(self, "state", "menu") or setattr(self, "input_text", ""))

    def add_item(self):
        try:
            raw = self.input_text.strip()
            if not raw:
                self.show_toast("Digite os dados do item.")
                return
            parts = raw.split(":", 1)
            if len(parts) < 2:
                self.show_toast("Formato inválido. Use 'Book: ...' ou 'Magazine: ...'")
                return
            type_, details_str = parts[0].strip().lower(), parts[1].strip()
            # Support PT-BR aliases
            if type_ in ("livro",):
                type_ = "book"
            if type_ in ("revista",):
                type_ = "magazine"

            details = [d.strip() for d in details_str.split(",")]
            item_id = f"item_{random.randint(1000, 9999)}"
            created = False
            if type_ == "book" and len(details) == 3:
                self.library.add_item(Book(item_id, details[0], details[1], details[2]))
                created = True
            elif type_ == "magazine" and len(details) == 2:
                self.library.add_item(Magazine(item_id, details[0], details[1]))
                created = True
            else:
                self.show_toast("Dados insuficientes para o tipo informado.")
                return

            if created:
                self.library.save_data()
                self.input_text = ""
                self.state = "items"
                self.show_toast("Item salvo com sucesso!")
        except Exception as e:
            self.show_toast("Erro ao salvar item.")

    def add_user(self):
        try:
            raw = self.input_text.strip()
            if not raw:
                self.show_toast("Digite os dados do usuário.")
                return
            parts = raw.split(":", 1)
            if len(parts) < 2:
                self.show_toast("Formato inválido. Use 'Student: Nome' ou 'Professor: Nome'")
                return
            type_, name = parts[0].strip().lower(), parts[1].strip()
            # Support PT-BR aliases and generic label
            if type_ in ("aluno", "estudante", "usuario", "usuário", "user"):
                type_ = "student"
            if type_ in ("professor",):
                type_ = "professor"

            user_id = f"user_{random.randint(1000, 9999)}"
            if type_ == "student" and name:
                self.library.add_user(Student(user_id, name))
            elif type_ == "professor" and name:
                self.library.add_user(Professor(user_id, name))
            else:
                self.show_toast("Dados insuficientes para o usuário.")
                return
            self.library.save_data()
            self.input_text = ""
            self.state = "users"
            self.show_toast("Usuário salvo com sucesso!")
        except Exception as e:
            msg = str(e)
            if len(msg) > 80:
                msg = msg[:77] + "..."
            self.show_toast(f"Erro ao salvar usuário: {msg}")

    def process_loan(self):
        try:
            transaction_id = f"loan_{random.randint(1000, 9999)}"
            transaction = Loan(transaction_id, self.selected_user, self.selected_item)
            self.library.process_transaction(transaction)
            self.library.save_data()
            self.show_toast("Empréstimo salvo.")
            # Clear selections after successful loan
            self.selected_user = None
            self.selected_item = None
        except Exception:
            self.show_toast("Erro ao salvar empréstimo.")

    def process_return(self):
        try:
            transaction_id = f"return_{random.randint(1000, 9999)}"
            transaction = Return(transaction_id, self.selected_user, self.selected_item)
            self.library.process_transaction(transaction)
            self.library.save_data()
            self.show_toast("Devolução salva.")
        except Exception:
            self.show_toast("Erro ao salvar devolução.")

    def process_return_for(self, user, item):
        try:
            transaction_id = f"return_{random.randint(1000, 9999)}"
            transaction = Return(transaction_id, user, item)
            self.library.process_transaction(transaction)
            self.library.save_data()
            self.show_toast("Empréstimo finalizado.")
        except Exception:
            self.show_toast("Erro ao finalizar empréstimo.")