# Techlog Solutions — estudo com FastAPI

Projeto de aprendizado focado em **FastAPI**: API REST simples no estilo de um CRM, com rotas de clientes persistidos em **SQLite** (`techlog.db` na raiz do projeto).

## O que tem aqui

- **`app/main.py`** — aplicação FastAPI, health check (`/`), página HTML de exemplo (`/front`) e documentação automática.
- **`app/rotas/cliente.py`** — CRUD de clientes sob o prefixo `/clientes`.
- **`app/banco_de_dados/`** — conexão local (`BancoLocal`) e repositório assíncrono (`ClienteRepositorio`).
- **`app/modelos/cliente.py`** — modelos Pydantic.
- **`app/dependencias.py`** — injeção de dependências (FastAPI `Depends`).
- **`chamados.http`** — exemplos para a extensão **REST Client** / **HTTP Client** do editor.

## Pré-requisitos

- **Python** 3.14 ou superior (conforme `pyproject.toml`).
- **[uv](https://docs.astral.sh/uv/)** para ambiente virtual e dependências.

## Comandos essenciais

Na pasta do projeto:

```bash
# Instalar dependências (cria/atualiza o ambiente .venv)
uv sync

# Criar a tabela `clientes` no SQLite (rode uma vez, ou após apagar techlog.db)
uv run python -c "from app.banco_de_dados.local import BancoLocal; BancoLocal().inicializar_banco()"

# Subir a API com recarregamento ao editar código
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

O módulo da aplicação é **`app.main:app`** (arquivo `app/main.py`, variável `app`).

## Testar no navegador

Com o servidor rodando, abra:

| URL | Descrição |
|-----|-----------|
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/) | Health check (`{"status":"ok"}`) |
| [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | **Swagger UI** — ideal para testar POST, PUT, DELETE com formulários |
| [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) | **ReDoc** — documentação alternativa |
| [http://127.0.0.1:8000/front](http://127.0.0.1:8000/front) | Página HTML simples de exemplo |
| [http://127.0.0.1:8000/clientes](http://127.0.0.1:8000/clientes) | Lista de clientes (JSON) |

Para rotas que exigem corpo (criar/atualizar cliente), o caminho mais prático no navegador é usar o **Swagger** em `/docs`.

## Testar com arquivo `.http`

Abra `chamados.http` no Cursor/VS Code com uma extensão de cliente HTTP e execute as requisições (com o servidor em `127.0.0.1:8000`).

## Dependências principais

- **fastapi** — framework web e validação com Pydantic.
- **uvicorn** — servidor ASGI que executa a aplicação.

O módulo **`sqlite3`** faz parte da biblioteca padrão do Python; não entra no `pyproject.toml`.

## Problemas comuns

### Porta 8000 já em uso (`WinError 10048` / `Errno 10048`)

Se ao subir o uvicorn aparecer algo como *“normalmente é permitida apenas uma utilização de cada endereço de soquete”* ou *`error while attempting to bind on address ('127.0.0.1', 8000)`*, a **porta 8000 já está ocupada** por outro processo (muito comum: outra instância do uvicorn ainda rodando em outro terminal, ou um processo que não foi encerrado direito).

**1. Encerrar o servidor da forma correta**  
No terminal onde o uvicorn está ativo, use **Ctrl+C** e espere a mensagem de shutdown. Só então suba de novo com o mesmo comando.

**2. Descobrir qual processo usa a porta 8000 (Windows)**  
No PowerShell ou CMD:

```powershell
netstat -ano | findstr ":8000"
```

Procure a linha com estado **`LISTENING`**. O **PID** (última coluna) é o identificador do processo. Para encerrá-lo:

```powershell
taskkill /PID <número_do_pid> /F
```

Substitua `<número_do_pid>` pelo valor que apareceu no `netstat`. Depois disso, `uv run uvicorn ... --port 8000` deve voltar a funcionar.

**3. Usar outra porta (sem matar processo)**  
Se preferir não encerrar o que já está na 8000, suba em outra porta, por exemplo **8001**:

```bash
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

Nesse caso, troque todas as URLs de teste de `8000` para `8001` (por exemplo `http://127.0.0.1:8001/docs`).
