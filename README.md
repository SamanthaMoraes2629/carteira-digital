# 💳 Carteira Digital - Backend

**Sistema backend desenvolvido em Python utilizando SQLModel para gerenciamento de contas bancárias, controle de saldo, movimentações financeiras e geração de relatórios com histórico e gráficos. A aplicação segue os princípios de modularização e separação de responsabilidades (MVC simplificado).**

## 🚀 Funcionalidades

 Criação de contas bancárias únicas por instituição

- Desativação de contas com verificação de saldo

- Transferência de valores entre contas

- Movimentações financeiras (depósitos)

- Geração de gráficos e relatórios históricos (em desenvolvimento)

- Armazenamento persistente em banco de dados via SQLModel

## ⚙️ Tecnologias Utilizadas

- Python 3.11+

- SQLModel (ORM baseada em SQLAlchemy + Pydantic)

- SQLite (padrão, substituível por qualquer outro banco compatível com SQLAlchemy)

- Matplotlib (para geração de gráficos, se ativado)

- IOWrapper (para garantir compatibilidade UTF-8)

## 🧱 Estrutura do Projeto

```bash

carteira_digital/
├── models.py         # Definições das classes de dados (Conta, Histórico, Enum Bancos)
├── view.py           # Funções lógicas de manipulação de dados (controlador)
├── templates.py      # Interface de terminal (UI)
├── database.db       # Banco de dados SQLite (gerado automaticamente)
└── ...
```

## 📌 Comandos disponíveis via UI (terminal)
Ao executar o templates.py, o sistema exibe o seguinte menu:

csharp
Copiar
Editar
[1] -> Criar conta
[2] -> Desativar conta
[3] -> Transferir dinheiro
[4] -> Movimentar dinheiro
[5] -> Total contas
[6] -> Filtrar histórico
[7] -> Gráfico
Cada opção executa operações CRUD seguras com validações completas e feedback ao usuário.

## 🛠️ Como executar localmente
Clone o repositório:

```bash

git clone https://github.com/seu-usuario/carteira-digital.git
cd carteira-digital
Crie um ambiente virtual e instale as dependências:
```

```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
Execute a aplicação via terminal:
```

```bash

python templates.py
Certifique-se de ter o Python 3.11+ instalado.
```

## 📈 Em desenvolvimento
- Filtros avançados por data e tipo de transação

- Exportação de histórico financeiro

- Integração com frontend (futuro)

- Dashboard com gráficos via Web

 
