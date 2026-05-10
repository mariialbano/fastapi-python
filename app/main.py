from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import (  # Importação para retornar HTML como response
    HTMLResponse,
)
from fastapi.staticfiles import StaticFiles

# Importação do Jinja para construção do Front-End usando Python.
from fastapi.templating import (
    Jinja2Templates,
)

from app.dependencias import banco_de_dados
from app.rotas import cliente, login, logout, registro
from app.rotas.autenticacao_middleware import AuthenticationToken

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(_application: FastAPI):
    banco_de_dados.inicializar_banco()
    yield


app = FastAPI(
    title="Techlog Solutions API (Alura)",
    description="CRM para Techlog Solutions",
    version="0.0.1",
    lifespan=lifespan,
)

app.mount(
    "/static", StaticFiles(directory="static"), name="static"
)  # mapeamento da pasta Static
app.add_middleware(AuthenticationToken)
app.include_router(cliente.router)  # Rotas do Back
app.include_router(cliente.front_router)  # Rotas do Front
app.include_router(login.router)
app.include_router(registro.router)
app.include_router(logout.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
# Edição no endpoint de /frontend para /.
# Normalmente a primeira página de um website é o front.
async def frontend(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"titulo": "Techlog Solutions CRM", "versao": "1.0.0"},
    )
