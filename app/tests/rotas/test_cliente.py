import pytest
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.modelos.cliente import Cliente, ClienteCriarAtualizar
from app.rotas.cliente import (
    atualizar_cliente,
    criar_cliente,
    deletar_cliente,
    listar_clientes,
    obter_cliente,
    pagina_listar_clientes,
)


class TestRotasCliente:
    @pytest.mark.asyncio
    async def test_listar_clientes(self, mock_cliente_repositorio):
        clientes = [
            Cliente(
                id_=1,
                nome="Cliente 1",
                email="c1@example.com",
                telefone="111",
            )
        ]
        mock_cliente_repositorio.listar_clientes.return_value = clientes

        resultado = await listar_clientes(mock_cliente_repositorio)

        assert resultado == clientes
        mock_cliente_repositorio.listar_clientes.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_obter_cliente_retorna_cliente(self, mock_cliente_repositorio):
        cliente = Cliente(
            id_=1,
            nome="Cliente 1",
            email="c1@example.com",
            telefone="111",
        )
        mock_cliente_repositorio.obter_cliente.return_value = cliente

        resultado = await obter_cliente(mock_cliente_repositorio, 1)

        assert resultado == cliente
        mock_cliente_repositorio.obter_cliente.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_obter_cliente_levanta_404(self, mock_cliente_repositorio):
        mock_cliente_repositorio.obter_cliente.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await obter_cliente(mock_cliente_repositorio, 99)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Cliente não encontrado"

    @pytest.mark.asyncio
    async def test_criar_cliente(self, mock_cliente_repositorio):
        dados = ClienteCriarAtualizar(
            nome="Novo",
            email="novo@example.com",
            telefone="222",
        )
        cliente_criado = Cliente(id_=2, **dados.model_dump())
        mock_cliente_repositorio.criar_cliente.return_value = cliente_criado

        resultado = await criar_cliente(mock_cliente_repositorio, dados)

        assert resultado == cliente_criado
        mock_cliente_repositorio.criar_cliente.assert_awaited_once_with(dados)

    @pytest.mark.asyncio
    async def test_atualizar_cliente_retorna_cliente(self, mock_cliente_repositorio):
        dados = ClienteCriarAtualizar(
            nome="Atualizado",
            email="atualizado@example.com",
            telefone="333",
        )
        cliente_atualizado = Cliente(id_=1, **dados.model_dump())
        mock_cliente_repositorio.atualizar_cliente.return_value = cliente_atualizado

        resultado = await atualizar_cliente(mock_cliente_repositorio, dados, 1)

        assert resultado == cliente_atualizado
        mock_cliente_repositorio.atualizar_cliente.assert_awaited_once_with(dados, 1)

    @pytest.mark.asyncio
    async def test_atualizar_cliente_levanta_404(self, mock_cliente_repositorio):
        dados = ClienteCriarAtualizar(
            nome="Atualizado",
            email="atualizado@example.com",
            telefone="333",
        )
        mock_cliente_repositorio.atualizar_cliente.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await atualizar_cliente(mock_cliente_repositorio, dados, 99)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_deletar_cliente_com_sucesso(self, mock_cliente_repositorio):
        mock_cliente_repositorio.deletar_cliente.return_value = True

        resultado = await deletar_cliente(mock_cliente_repositorio, 1)

        assert resultado is None
        mock_cliente_repositorio.deletar_cliente.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_deletar_cliente_levanta_404(self, mock_cliente_repositorio):
        mock_cliente_repositorio.deletar_cliente.return_value = False

        with pytest.raises(HTTPException) as exc_info:
            await deletar_cliente(mock_cliente_repositorio, 99)

        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_pagina_listar_clientes(self, mock_cliente_repositorio, mock_request):
        clientes = [
            Cliente(
                id_=1,
                nome="Cliente 1",
                email="c1@example.com",
                telefone="111",
            )
        ]
        mock_cliente_repositorio.listar_clientes.return_value = clientes

        resultado = await pagina_listar_clientes(mock_request, mock_cliente_repositorio)

        assert isinstance(resultado, HTMLResponse)
        assert resultado.context["clientes"] == clientes
        assert resultado.context["titulo"] == "Lista de Clientes"
