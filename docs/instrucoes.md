# Setup do Ambiente Virtual (venv)

Explica como configurar o ambiente virtual do projeto, instalar as dependências e preparar o ambiente de desenvolvimento local.

## ✅ Passo a passo

### 1. Criar o ambiente virtual
```bash
python -m venv venv
```
Vai criar ma pasta chamada venv/ com os arquivos do ambiente isolado.

### 2. Ativar ambiente virtual (no Windows)
```bash
venv\Scripts\activate
```
O terminal deve mostrar algo do tipo (venv) se tiver dado certo.
### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```
### 4. Atualizar o requirements.txt após instalar novas libs
Teoricamente opcional, mas como vamos usar várias bibliotecas é bom usar.
```bash
pip freeze > requirements.txt
```
