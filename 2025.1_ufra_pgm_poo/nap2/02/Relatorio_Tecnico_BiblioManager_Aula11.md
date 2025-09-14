# Relatório Técnico — BiblioManager (Aula 11)
_Gerado em 09/09/2025 17:33._

Este relatório descreve a estrutura do código encontrado no arquivo **atividade 11 .zip**, mapeando módulos, classes e funções, e avaliando a aderência aos requisitos da Atividade (PDF). Também apresenta um passo a passo de execução e observações técnicas.

## Checklist de Requisitos (conforme PDF)
- Abstração com `abc` e classes abstratas: ✅ Atende
- Hierarquia base (`LibraryEntity` → `Item`/`User` e `Transaction`): ✅ Atende
- Subclasses de Itens (`Book`, `Magazine`, `DVD`): ✅ Atende
- Subclasses de Usuários (`Student`, `Professor`, `Visitor`): ✅ Atende
- Subclasses de Transações (`Loan`, `Return`, `Reservation`): ✅ Atende
- Encapsulamento/Status com `@property`: ✅ Atende
- GUI em Pygame (1024×768) e menu com botões: 🟨 Parcial / a verificar / ✅ Atende
- Persistência em JSON (salvar/carregar): ✅ Atende
- Formulários (inputs) na GUI: ✅ Atende
- Validações (`validate()` por entidade): ✅ Atende
- Relatórios/Gráficos (barras): ✅ Atende

> **Observação**: o código contém trechos com `...` (Ellipsis) usados como _placeholders_. Isso é **válido** em Python (equivalente a um `pass`), porém pode indicar funcionalidades ainda **incompletas** (por exemplo, `update_status` em algumas classes). Em runtime, tais métodos não executam lógica além do _placeholder_.
## Módulos e Estrutura

### atividade 11 enviar no grupo/charts_demo.py
- Linhas: `25` — SHA: `ffeac4473b`
- (Sem classes — possivelmente utilitário ou script)

### atividade 11 enviar no grupo/main.py
- Linhas: `13` — SHA: `817357b55f`
- (Sem classes — possivelmente utilitário ou script)

### atividade 11 enviar no grupo/models/__init__.py
- Linhas: `1` — SHA: `73e45cab0b`
- (Sem classes — possivelmente utilitário ou script)

### atividade 11 enviar no grupo/models/entities.py
- Linhas: `42` — SHA: `45af8005c8`
- Classes:
  - **LibraryEntity**
    - Métodos: __init__, id, status, status, display_info, update_status, validate, serialize

### atividade 11 enviar no grupo/models/items.py
- Linhas: `57` — SHA: `624abaf3d0`
- Classes:
  - **Item**
    - Métodos: __init__
  - **Book**
    - Métodos: __init__, display_info, update_status, validate, serialize
  - **Magazine**
    - Métodos: __init__, display_info, update_status, validate, serialize
  - **DVD**
    - Métodos: __init__, display_info, update_status, validate, serialize

### atividade 11 enviar no grupo/models/transactions.py
- Linhas: `64` — SHA: `058e68ebc9`
- Classes:
  - **Transaction**
    - Métodos: __init__, process
  - **Loan**
    - Métodos: display_info, update_status, validate, serialize, process
  - **Return**
    - Métodos: display_info, update_status, validate, serialize, process
  - **Reservation**
    - Métodos: display_info, update_status, validate, serialize, process

### atividade 11 enviar no grupo/models/users.py
- Linhas: `54` — SHA: `a10e4e2fdc`
- Classes:
  - **User**
    - Métodos: __init__
  - **Student**
    - Métodos: __init__, display_info, update_status, validate, serialize
  - **Professor**
    - Métodos: __init__, display_info, update_status, validate, serialize
  - **Visitor**
    - Métodos: __init__, display_info, update_status, validate, serialize

### atividade 11 enviar no grupo/ui/__init__.py
- Linhas: `1` — SHA: `cffa9c4863`
- (Sem classes — possivelmente utilitário ou script)

### atividade 11 enviar no grupo/ui/app.py
- Linhas: `1263` — SHA: `5541dc5147`
- Classes:
  - **Button**
    - Métodos: __init__, draw, handle_event
  - **InputField**
    - Métodos: __init__, draw, handle_event
  - **BiblioApp**
    - Métodos: __init__, load_data, save_data, _build_navbar, _go, _count_items, _count_users, _add_build_fields, _add_validate, _add_save, render_add_item, handle_add_item_event, _user_build_fields, _user_limit_default, _user_normalize_limits, _user_validate, _user_save, _user_delete, _user_start_edit, _user_apply_edit, render_manage_users, handle_manage_users_event, _loan_lists, _loan_can_borrow, _loan_do_borrow, _loan_do_return, _loan_do_reserve, render_loans, handle_loans_event, _rep_filtered_items, _rep_export_json, _rep_export_csv, _rep_group_by_user, _rep_export_by_user_json, _rep_export_by_user_csv, render_reports, handle_reports_event, _item_build_fields_from, _item_validate_inputs, _item_apply_edit, _item_delete_selected, render_shelf, render_dashboard, render_navbar, render_placeholder, run, _draw_exit_btn, draw_navbar, draw_navbar

### atividade 11 enviar no grupo/ui/ui_charts.py
- Linhas: `51` — SHA: `7e6a5a5dac`
- (Sem classes — possivelmente utilitário ou script)

### atividade 11 enviar no grupo/ui/ui_nav.py
- Linhas: `13` — SHA: `ee6f607b7b`
- (Sem classes — possivelmente utilitário ou script)

## Passo a passo (execução e fluxo)
1. **Inicialização**: `main.py` importa `BiblioApp` (`ui/app.py`) e chama `app.run()` — abre janela **1024×768** (Pygame).
2. **Navegação**: barra/menu com botões _Adicionar Item_, _Gerenciar Usuários_, _Empréstimos_, _Relatórios_ e _Sair_.
3. **Formulários**: componentes de entrada via `InputField` processam `KEYDOWN` e `MOUSEBUTTONDOWN`.
4. **POO**:
   - `LibraryEntity` (abstrata) define `id` auto-incremental, `created_at`, `status` com `@property/@setter`, e métodos abstratos `display_info`, `update_status`, `validate`, `serialize`.
   - `Item` → `Book`, `Magazine`, `DVD` — cada um implementa `display_info`/`serialize` e aceita `update_status`.
   - `User` → `Student`, `Professor`, `Visitor` — guarda `limit` e `display_info`; `validate` simples.
   - `Transaction` (abstrata) → `Loan`, `Return`, `Reservation`, com `process(user, item)`.
5. **Persistência**: uso de `json.load/json.dump` para ler/escrever `data/library_data.json` (itens, usuários, transações).
6. **Relatórios/Gráficos**: `ui/ui_charts.py` fornece `draw_bar_chart()` (barras) — usado para estatísticas como _Itens por Tipo_, _Status_, _Uso por Usuário_.
7. **Saída**: botão **Sair** utilitário em `ui/ui_nav.py` (além de handlers de eventos).

## Observações técnicas e limitações
- Há **placeholders (`...`)** em métodos de várias classes (ex.: `update_status` em `Loan/Return`, `Book`, etc.). Isso não quebra a execução, mas significa que parte da **lógica de negócio** pode estar **incompleta** (ex.: validação de disponibilidade/limite, atualização de status e registro de transação).
- Não foi possível confirmar por leitura estática a presença de **rolagem** em listas longas (requisito opcional da GUI), embora existam manejos de `MOUSEBUTTONDOWN` e inputs.
- Recomenda-se finalizar:
  - Lógicas de `process()` para **empréstimo/devolução/reserva** (checar `status` do item e `limit` do usuário, registrar histórico).
  - Rotinas de **relatório** com agregações (contagens por tipo/status/usuário) — `draw_bar_chart` já está pronto.
  - Mensagens de erro/feedback (ex.: empréstimo de item indisponível, limite excedido).

## Como executar (Windows)
- Use `start.bat` (cria venv, instala `pygame`, executa `main.py`) ou:
  ```bat
  pip install pygame
  python main.py
  ```

