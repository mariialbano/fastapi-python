from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio
from app.modelos.usuario import UsuarioCriarAtualizar

templates = Jinja2Templates(directory="templates")


class FormularioRegistro(BaseModel):
    nome: str
    email: str
    senha: str
    confirma_senha: str


router = APIRouter(prefix="/registro")


def _resposta_erro(request: Request, nome: str, email: str, erro: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "registro.html",
        {"nome": nome, "email": email, "error": erro},
    )


@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(
        request,
        "registro.html",
        {"nome": "", "email": ""},
    )


@router.post("/")
async def registrar_usuario(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
    request: Request,
    formulario: Annotated[FormularioRegistro, Form()],
):
    nome_limpo = formulario.nome.strip()
    email_limpo = formulario.email.strip()
    senha = formulario.senha
    confirma_senha = formulario.confirma_senha

    if not nome_limpo or not email_limpo or not senha or not confirma_senha:
        return _resposta_erro(
            request,
            nome_limpo,
            email_limpo,
            "Todos os campos são obrigatórios.",
        )

    if len(senha) < 6:
        return _resposta_erro(
            request,
            nome_limpo,
            email_limpo,
            "A senha deve ter pelo menos 6 caracteres.",
        )

    if senha != confirma_senha:
        return _resposta_erro(
            request,
            nome_limpo,
            email_limpo,
            "As senhas não conferem.",
        )

    if await usuario_repositorio.existe_email(email_limpo):
        return _resposta_erro(
            request,
            nome_limpo,
            email_limpo,
            "Já existe uma conta com este e-mail.",
        )

    dados = UsuarioCriarAtualizar(nome=nome_limpo, email=email_limpo, senha=senha)
    await usuario_repositorio.criar_usuario(dados)
    return RedirectResponse(url="/login", status_code=303)
