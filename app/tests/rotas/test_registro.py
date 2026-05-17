import pytest
from fastapi.responses import HTMLResponse, RedirectResponse

from app.rotas.registro import FormularioRegistro, pagina_registro, registrar_usuario


class TestRotasRegistro:
    @pytest.mark.asyncio
    async def test_pagina_registro(self, mock_request):
        resultado = await pagina_registro(mock_request)

        assert isinstance(resultado, HTMLResponse)
        assert resultado.template.name == "registro.html"
        assert resultado.context["nome"] == ""
        assert resultado.context["email"] == ""

    @pytest.mark.asyncio
    async def test_registrar_usuario_com_campos_vazios(
        self, mock_usuario_repositorio, mock_request
    ):
        formulario = FormularioRegistro(
            nome="  ",
            email="",
            senha="",
            confirma_senha="",
        )

        resultado = await registrar_usuario(
            mock_usuario_repositorio, mock_request, formulario
        )

        assert isinstance(resultado, HTMLResponse)
        assert resultado.context["error"] == "Todos os campos são obrigatórios."
        mock_usuario_repositorio.criar_usuario.assert_not_called()

    @pytest.mark.asyncio
    async def test_registrar_usuario_com_senha_curta(
        self, mock_usuario_repositorio, mock_request
    ):
        formulario = FormularioRegistro(
            nome="Maria",
            email="maria@example.com",
            senha="12345",
            confirma_senha="12345",
        )

        resultado = await registrar_usuario(
            mock_usuario_repositorio, mock_request, formulario
        )

        assert isinstance(resultado, HTMLResponse)
        assert resultado.context["error"] == "A senha deve ter pelo menos 6 caracteres."

    @pytest.mark.asyncio
    async def test_registrar_usuario_com_senhas_diferentes(
        self, mock_usuario_repositorio, mock_request
    ):
        formulario = FormularioRegistro(
            nome="Maria",
            email="maria@example.com",
            senha="senha123",
            confirma_senha="outrasenha",
        )

        resultado = await registrar_usuario(
            mock_usuario_repositorio, mock_request, formulario
        )

        assert isinstance(resultado, HTMLResponse)
        assert resultado.context["error"] == "As senhas não conferem."

    @pytest.mark.asyncio
    async def test_registrar_usuario_com_email_ja_cadastrado(
        self, mock_usuario_repositorio, mock_request
    ):
        mock_usuario_repositorio.existe_email.return_value = True
        formulario = FormularioRegistro(
            nome="Maria",
            email="maria@example.com",
            senha="senha123",
            confirma_senha="senha123",
        )

        resultado = await registrar_usuario(
            mock_usuario_repositorio, mock_request, formulario
        )

        assert isinstance(resultado, HTMLResponse)
        assert resultado.context["error"] == "Já existe uma conta com este e-mail."
        mock_usuario_repositorio.criar_usuario.assert_not_called()

    @pytest.mark.asyncio
    async def test_registrar_usuario_com_sucesso(
        self, mock_usuario_repositorio, mock_request
    ):
        mock_usuario_repositorio.existe_email.return_value = False
        formulario = FormularioRegistro(
            nome="Maria",
            email="maria@example.com",
            senha="senha123",
            confirma_senha="senha123",
        )

        resultado = await registrar_usuario(
            mock_usuario_repositorio, mock_request, formulario
        )

        assert isinstance(resultado, RedirectResponse)
        assert resultado.status_code == 303
        assert resultado.headers["location"] == "/login"
        mock_usuario_repositorio.existe_email.assert_awaited_once_with(
            "maria@example.com"
        )
        mock_usuario_repositorio.criar_usuario.assert_awaited_once()
