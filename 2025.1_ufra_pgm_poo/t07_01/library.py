import json
from entities import Book, Magazine, Student, Professor, Loan, Return

class Library:
    """Camada de dados simples da aplicação.

    Responsabilidades:
    - Armazenar itens, usuários e transações em memória
    - Oferecer operações para adicionar/atualizar/excluir
    - Salvar e carregar os dados do arquivo JSON
    """
    def __init__(self):
        self.__items = {}
        self.__users = {}
        self.__transactions = {}
        self.load_data()

    def add_item(self, item):
        """Adiciona um item ao repositório (chave é o id do item)."""
        self.__items[item.id] = item

    def add_user(self, user):
        """Adiciona um usuário ao repositório (chave é o id do usuário)."""
        self.__users[user.id] = user

    def process_transaction(self, transaction):
        """Executa a transação (process) e a registra."""
        transaction.process()
        self.__transactions[transaction.id] = transaction

    def get_items(self):
        """Retorna a lista de itens (valores do dicionário)."""
        return list(self.__items.values())

    def get_users(self):
        """Retorna a lista de usuários (valores do dicionário)."""
        return list(self.__users.values())

    def get_transactions(self):
        """Retorna a lista de transações processadas."""
        return list(self.__transactions.values())

    def update_item(self, item_id, new_data):
        """Atualiza um item recriando a entidade com os novos dados."""
        if item_id not in self.__items:
            raise KeyError("Item not found")
        t = new_data.get("type")
        if t == "book":
            from entities import Book
            self.__items[item_id] = Book(item_id, new_data["name"], new_data["author"], new_data["isbn"])
        elif t == "magazine":
            from entities import Magazine
            self.__items[item_id] = Magazine(item_id, new_data["name"], new_data["edition"])
        else:
            raise ValueError("Unknown item type")

    def update_user(self, user_id, new_data):
        """Atualiza usuário recriando a entidade e preservando itens emprestados."""
        if user_id not in self.__users:
            raise KeyError("User not found")
        old = self.__users[user_id]
        t = new_data.get("type")
        if t == "student":
            from entities import Student
            updated = Student(user_id, new_data["name"])
        elif t == "professor":
            from entities import Professor
            updated = Professor(user_id, new_data["name"])
        else:
            raise ValueError("Unknown user type")
        # preserva itens emprestados
        for it in old.borrowed_items:
            updated.borrow_item(it)
        self.__users[user_id] = updated

    def delete_item(self, item_id):
        """Exclui item se não houver empréstimo em aberto (status borrowed)."""
        item = self.__items.get(item_id)
        if not item:
            raise KeyError("Item not found")
        if getattr(item, 'status', 'available') == 'borrowed':
            raise ValueError("Item has an open loan and cannot be deleted")
        del self.__items[item_id]

    def delete_user(self, user_id):
        """Exclui usuário se não houver empréstimos em aberto (lista borrowed_items)."""
        user = self.__users.get(user_id)
        if not user:
            raise KeyError("User not found")
        if getattr(user, 'borrowed_items', []):
            if len(user.borrowed_items) > 0:
                raise ValueError("User has open loans and cannot be deleted")
        del self.__users[user_id]

    def generate_report(self):
        """Retorna um texto com informações de itens e usuários."""
        report = []
        for item in self.__items.values():
            report.append(item.display_info())
        for user in self.__users.values():
            report.append(user.display_info())
        return "\n".join(report)

    def save_data(self):
        """Salva o estado atual em library_data.json."""
        data = {
            "items": [item.serialize() for item in self.__items.values()],
            "users": [user.serialize() for user in self.__users.values()],
            "transactions": [t.serialize() for t in self.__transactions.values()]
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        """Carrega library_data.json e reconstrói os objetos de domínio."""
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
            for item_data in data.get("items", []):
                if item_data["type"] == "book":
                    item = Book(item_data["id"], item_data["name"], item_data["author"], item_data["isbn"])
                elif item_data["type"] == "magazine":
                    item = Magazine(item_data["id"], item_data["name"], item_data["edition"])
                item.update_status(item_data["status"])
                self.__items[item_data["id"]] = item
            for user_data in data.get("users", []):
                if user_data["user_type"] == "student":
                    user = Student(user_data["id"], user_data["name"])
                elif user_data["user_type"] == "professor":
                    user = Professor(user_data["id"], user_data["name"])
                for item_id in user_data["borrowed_items"]:
                    if item_id in self.__items:
                        user.borrow_item(self.__items[item_id])
                # Restaura status, se existir
                if "status" in user_data:
                    user.update_status(user_data["status"])
                self.__users[user_data["id"]] = user
            for t_data in data.get("transactions", []):
                user = self.__users.get(t_data["user_id"])
                item = self.__items.get(t_data["item_id"])
                if user and item:
                    t_type = t_data.get("type")
                    if t_type == "Loan":
                        transaction = Loan(t_data["id"], user, item)
                    elif t_type == "Return":
                        transaction = Return(t_data["id"], user, item)
                    else:
                        # Fallback para dados antigos
                        transaction = Loan(t_data["id"], user, item) if t_data["id"].startswith("loan_") else Return(t_data["id"], user, item)
                    transaction.update_status(t_data.get("status", "completed"))
                    self.__transactions[t_data["id"]] = transaction
        except FileNotFoundError:
            pass