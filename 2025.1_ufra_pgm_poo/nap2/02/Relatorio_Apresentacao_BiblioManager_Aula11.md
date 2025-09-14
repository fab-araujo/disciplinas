# Roteiro de Apresentação — BiblioManager (até 20 min)

## 1) Contexto e Objetivo (1–2 min)
- Atividade Avaliativa 07 — **Gerenciamento de Biblioteca GUI** em Pygame.
- Objetivo: CRUD (itens/usuários), transações (empréstimo/devolução/reserva), relatórios, persistência JSON, POO (abstração, herança, polimorfismo, encapsulamento).

## 2) Arquitetura POO (4–5 min)
- **Abstração**: `LibraryEntity` e `Transaction` (métodos abstratos).
- **Herança**:
  - `LibraryEntity` → `Item`/`User`
  - `Item` → `Book`, `Magazine`, `DVD`
  - `User` → `Student`, `Professor`, `Visitor`
  - `Transaction` → `Loan`, `Return`, `Reservation`
- **Encapsulamento**: `__id`, `__status` com `@property/@setter`.
- **Polimorfismo**: `display_info()` e `serialize()` especializados por classe.

## 3) GUI em Pygame (3–4 min)
- Janela 1024×768, menu com: _Adicionar Item_, _Gerenciar Usuários_, _Empréstimos_, _Relatórios_, _Sair_.
- **Formulários** (`InputField`) para cadastro/edição.
- **Relatórios** com `draw_bar_chart()` (barras) — Itens por Tipo, Status, Uso por Usuário.
- Feedback visual (cores; botão Sair).

## 4) Persistência e Fluxo de Dados (3–4 min)
- Arquivo `data/library_data.json` contendo `items`, `users`, `transactions`.
- Carregamento inicial → manipulação em memória → salvamento com `json.dump` ao encerrar/confirmar.

## 5) Demonstração (4–5 min)
- Cadastro de um **Livro**, um **Estudante**.
- Em **Empréstimos**: seleção do usuário e do item → **Emprestar** → ver atualização de status.
- Abrir **Relatórios** e exibir os gráficos.
- Encerrar pelo botão **Sair**.

## 6) Limitações e Próximos Passos (1–2 min)
- Métodos com `...` ainda não implementam toda a lógica (limites, checagem de disponibilidade, mensagens de erro).
- Próximos passos: completar `process()` de `Loan/Return/Reservation`, validar `limit`, melhorar feedback e rolagem de listas.

## 7) Conclusão (30–60s)
- Estrutura POO e GUI já consolidadas; persistência e relatórios prontos para expansão.
- O projeto **atende estruturalmente** aos requisitos principais e está **quase pronto** funcionalmente, exigindo apenas finalizar regras de negócio nas transações.
