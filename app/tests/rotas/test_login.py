import pytest
from fastapi.responses import HTMLResponse, RedirectResponse

from app.modelos.usuario import Usuario
from app.rotas.autenticacao_middleware import VALOR_TOKEN_SESSAO
from app.rotas.login import login, pagina_login


class TestRotasLogin:
    @pytest.mark.asyncio
    async def test_pagina_login(self, mock_request):
        resultado = await pagina_login(mock_request)

        assert isinstance(resultado, HTMLResponse)
        assert resultado.template.name == "login.html"

    @pytest.mark.asyncio
    async def test_login_com_credenciais_validas(
        self, mock_usuario_repositorio, mock_request
    ):
        usuario = Usuario(
            id_=1,
            nome="Maria",
            email="maria@example.com",
            senha="senha123",
        )
        mock_usuario_repositorio.buscar_usuario_email_senha.return_value = usuario

        resultado = await login(
            mock_usuario_repositorio,
            mock_request,
            email="maria@example.com",
            senha="senha123",
        )

        assert isinstance(resultado, RedirectResponse)
        assert resultado.status_code == 303
        assert resultado.headers["location"] == "/"
        assert resultado.headers["set-cookie"].startswith("session_token=")
        assert VALOR_TOKEN_SESSAO in resultado.headers["set-cookie"]
        mock_usuario_repositorio.buscar_usuario_email_senha.assert_awaited_once_with(
            "maria@example.com",
            "senha123",
        )

    @pytest.mark.asyncio
    async def test_login_com_credenciais_invalidas(
        self, mock_usuario_repositorio, mock_request
    ):
        mock_usuario_repositorio.buscar_usuario_email_senha.return_value = None

        resultado = await login(
            mock_usuario_repositorio,
            mock_request,
            email="errado@example.com",
            senha="senha",
        )

        assert isinstance(resultado, HTMLResponse)
        assert resultado.template.name == "login.html"
        assert resultado.context["email"] == "errado@example.com"
        assert resultado.context["senha"] == "senha"
        assert resultado.context["error"] == "Credenciais inválidas"
