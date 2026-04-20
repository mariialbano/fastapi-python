from typing import Annotated

from fastapi import Depends

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.banco_de_dados.local import BancoLocal
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio

banco_de_dados = BancoLocal()


def obter_banco_de_dados() -> BancoLocal:
    return banco_de_dados


def obter_cliente_repositorio(
    banco_de_dados_local: Annotated[BancoLocal, Depends(obter_banco_de_dados)],
) -> ClienteRepositorio:
    return ClienteRepositorio(banco_de_dados_local)


def obter_usuario_repositorio(
    banco_de_dados_local: Annotated[BancoLocal, Depends(obter_banco_de_dados)],
) -> UsuarioRepositorio:
    return UsuarioRepositorio(banco_de_dados_local)
