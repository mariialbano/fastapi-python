import pytest

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.modelos.cliente import Cliente, ClienteCriarAtualizar


@pytest.fixture
def cliente_repositorio(mock_banco_dados):
    return ClienteRepositorio(mock_banco_dados)


class TestClienteRepositorio:
    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_vazia(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchall.return_value = []

        resultado = await cliente_repositorio.listar_clientes()

        assert resultado == []
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email, telefone FROM clientes"
        )
        mock_banco_dados.cursor.fetchall.assert_called_once()

    @pytest.mark.asyncio
    async def test_listar_clientes_retorna_lista_com_clientes(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchall.return_value = [
            (1, "Cliente 1", "cliente1@example.com", "1234567890"),
            (2, "Cliente 2", "cliente2@example.com", "0987654321"),
        ]

        resultado = await cliente_repositorio.listar_clientes()

        assert len(resultado) == 2
        assert resultado[0] == Cliente(
            id_=1,
            nome="Cliente 1",
            email="cliente1@example.com",
            telefone="1234567890",
        )
        assert resultado[1] == Cliente(
            id_=2,
            nome="Cliente 2",
            email="cliente2@example.com",
            telefone="0987654321",
        )

    @pytest.mark.asyncio
    async def test_obter_cliente_retorna_cliente(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = (
            1,
            "Cliente 1",
            "cliente1@example.com",
            "1234567890",
        )

        resultado = await cliente_repositorio.obter_cliente(1)

        assert resultado == Cliente(
            id_=1,
            nome="Cliente 1",
            email="cliente1@example.com",
            telefone="1234567890",
        )
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "SELECT id, nome, email, telefone FROM clientes WHERE id = ?",
            (1,),
        )

    @pytest.mark.asyncio
    async def test_obter_cliente_retorna_none_quando_nao_existe(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.fetchone.return_value = None

        resultado = await cliente_repositorio.obter_cliente(99)

        assert resultado is None

    @pytest.mark.asyncio
    async def test_criar_cliente(self, cliente_repositorio, mock_banco_dados):
        mock_banco_dados.cursor.lastrowid = 3
        dados = ClienteCriarAtualizar(
            nome="Novo Cliente",
            email="novo@example.com",
            telefone="1111111111",
        )

        resultado = await cliente_repositorio.criar_cliente(dados)

        assert resultado == Cliente(
            id_=3,
            nome="Novo Cliente",
            email="novo@example.com",
            telefone="1111111111",
        )
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            ("Novo Cliente", "novo@example.com", "1111111111"),
        )

    @pytest.mark.asyncio
    async def test_atualizar_cliente_retorna_cliente_atualizado(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.rowcount = 1
        dados = ClienteCriarAtualizar(
            nome="Cliente Atualizado",
            email="atualizado@example.com",
            telefone="2222222222",
        )

        resultado = await cliente_repositorio.atualizar_cliente(dados, 1)

        assert resultado == Cliente(
            id_=1,
            nome="Cliente Atualizado",
            email="atualizado@example.com",
            telefone="2222222222",
        )

    @pytest.mark.asyncio
    async def test_atualizar_cliente_retorna_none_quando_nao_existe(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.rowcount = 0
        dados = ClienteCriarAtualizar(
            nome="Cliente",
            email="cliente@example.com",
            telefone="3333333333",
        )

        resultado = await cliente_repositorio.atualizar_cliente(dados, 99)

        assert resultado is None

    @pytest.mark.asyncio
    async def test_deletar_cliente_retorna_true_quando_exclui(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.rowcount = 1

        resultado = await cliente_repositorio.deletar_cliente(1)

        assert resultado is True
        mock_banco_dados.cursor.execute.assert_called_once_with(
            "DELETE FROM clientes WHERE id = ?", (1,)
        )

    @pytest.mark.asyncio
    async def test_deletar_cliente_retorna_false_quando_nao_existe(
        self, cliente_repositorio, mock_banco_dados
    ):
        mock_banco_dados.cursor.rowcount = 0

        resultado = await cliente_repositorio.deletar_cliente(99)

        assert resultado is False
