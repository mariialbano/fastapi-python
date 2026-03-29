from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.banco_de_dados.local import BancoLocal
from fastapi import Depends
from typing import Annotated

banco_de_dados = BancoLocal()

def obter_banco_de_dados() -> BancoLocal:
    return banco_de_dados

def obter_cliente_repositorio(banco_de_dados_local: Annotated[BancoLocal, Depends(obter_banco_de_dados)]) -> ClienteRepositorio:
    return ClienteRepositorio(banco_de_dados_local)