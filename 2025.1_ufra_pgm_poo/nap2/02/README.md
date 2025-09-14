# BiblioManager - Aula 11

Sistema de Gerenciamento de Biblioteca (GUI em Pygame).

## Funcionalidades (conforme atividade PDF)
- CRUD de Itens (Livro, Revista, DVD)
- CRUD de Usuários (Estudante, Professor, Visitante)
- Empréstimos, Devoluções e Reservas
- Relatórios básicos
- Persistência em JSON

## Execução
```bash
python main.py
```


## Navegação
- **Dashboard**: visão geral.
- **Prateleira**: grid de itens (role com a rodinha do mouse).
- **Adicionar Item / Gerenciar Usuários / Empréstimos / Relatórios**: telas placeholder para a apresentação (navegação pronta).

Use **ESC** para sair (salvamento automático).


## Funcionalidades implementadas
- **Adicionar Item** (Livro/Revista/DVD) com validação e persistência JSON.
- **Gerenciar Usuários** (cadastrar, listar, **remover** com Delete).
- **Empréstimos/Devoluções/Reservas**: seleciona usuário e item, atualiza status e registra em `transactions`.

## Dicas de uso
- Vá em **Gerenciar Usuários** para cadastrar pessoas (Student/Professor/Visitor).
- Em **Adicionar Item**, cadastre livros/revistas/DVDs.
- Em **Empréstimos**, clique para selecionar um usuário e um item e use os botões **Emprestar/Devolver/Reservar**.
- **ESC** para sair (salva automaticamente).


## Como executar (Windows/VS Code)
1. Abra o **Terminal** na pasta raiz do projeto (a que contém `main.py`):
   ```bash
   cd CAMINHO\Aula11_BiblioManager_FINAL
   python main.py
   ```
2. **Não** execute arquivos dentro de `models/` ou `ui/` diretamente (eles são módulos).
3. Se usar VS Code, abra a pasta do projeto (`File > Open Folder`), e rode `main.py`.
