import pytest

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


@pytest.fixture
def usuario_repositorio(mock_banco_dados):
    return UsuarioRepositorio(mock_banco_dados)


class TestUsuarioRepositorio:
    @pytest.mark.asyncio
    async def test_buscar_usuario_email_senha_retorna_usuario(
        self, usuario_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = (
            1,
            "Maria",
            "maria@example.com",
        )

        resultado = await usuario_repositorio.buscar_usuario_email_senha(
            "maria@example.com",
            "senha123",
        )

        assert resultado == Usuario(
            id_=1,
            nome="Maria",
            email="maria@example.com",
            senha="senha123",
        )
        mock_banco_dados.cursor.execute.assert_called_once_with(
            """SELECT id, nome, email FROM usuarios
                   WHERE lower(email) = lower(?) AND senha = ?""",
            ("maria@example.com", "senha123"),
        )

    @pytest.mark.asyncio
    async def test_buscar_usuario_email_senha_retorna_none(
        self, usuario_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = None

        resultado = await usuario_repositorio.buscar_usuario_email_senha(
            "inexistente@example.com",
            "senha",
        )

        assert resultado is None

    @pytest.mark.asyncio
    async def test_existe_email_retorna_true(
        self, usuario_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = (1,)

        resultado = await usuario_repositorio.existe_email("  usuario@example.com  ")

        assert resultado is True
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT 1 FROM usuarios WHERE lower(email) = lower(?)",
            ("usuario@example.com",),
        )

    @pytest.mark.asyncio
    async def test_existe_email_retorna_false(
        self, usuario_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = None

        resultado = await usuario_repositorio.existe_email("novo@example.com")

        assert resultado is False

    @pytest.mark.asyncio
    async def test_criar_usuario(self, usuario_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.lastrowid = 5
        dados = UsuarioCriarAtualizar(
            nome="  João  ",
            email="  Joao@Example.COM  ",
            senha="senha123",
        )

        resultado = await usuario_repositorio.criar_usuario(dados)

        assert resultado == Usuario(
            id_=5,
            nome="João",
            email="joao@example.com",
            senha="senha123",
        )
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            ("João", "joao@example.com", "senha123"),
        )
