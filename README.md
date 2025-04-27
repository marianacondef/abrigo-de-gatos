# tp2-adc
# 🐾 Abrigo de Gatos

Sistema de gerenciamento para um abrigo de gatos: controle de cadastros, medicações e processos de adoção.

## ✨ Funcionalidades

- Cadastro, edição e exclusão de gatos.
- Solicitação de adoções por usuários registrados.
- Aprovação ou recusa de adoções por administradores.
- Controle de medicações para os gatos.
- Filtros inteligentes por nome, idade, peso e status.
- Sistema de login para usuários comuns e administradores.

## 🚀 Como Rodar o Projeto

1. Clone o repositório:
   ```bash
   git clone [link-do-repositorio]

2. Acesse a pasta do projeto:
   ```bash 
   cd abrigo-de-gatos

3. Crie o ambiente virtual:
   ```bash
   python -m venv venv


---

```markdown
### ativar, instalar, rodar

4. Ative o ambiente virtual:
   - **Git Bash**:
     ```bash
     source "venv/Scripts/activate"
     ```
   - **PowerShell**:
     ```powershell
     .\venv\Scripts\activate
     ```

5. Instale as dependências:
   ```bash
   pip install flask flask-login flask-sqlalchemy flask-migrate

6. Rode o servidor:
    ```bash
    python run.py

7. Acesse no navegador:
    ```cpp
    http://127.0.0.1:5000/

```markdown
## 🛠️ Tecnologias Utilizadas

- Python 3.11
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite

```markdown
## 📂 Estrutura Básica do Projeto

```bash
tp2-adc/
├── app/
│   ├── models.py
│   ├── routes/
├── migrations/
├── venv/
├── config.py
├── run.py
├── abrigo.db
├── README.md
├── requirements.txt
└── static/
    ├── style.css

```markdown
## ⚡ Observações

- Banco de dados SQLite (`abrigo.db`) já configurado e pronto para uso.
- Projeto roda em modo `debug=True` para facilitar desenvolvimento (recarrega automático).
- Usuários e admins precisam ser registrados manualmente (via site).
