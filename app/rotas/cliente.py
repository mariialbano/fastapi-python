from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.modelos.cliente import Cliente, ClienteCriarAtualizar
from app.dependencias import obter_cliente_repositorio


clientes_list = [Cliente(id_=1, nome="João", email="joao@gmail.com", telefone="11999999999"),
    Cliente(id_=2, nome="Maria", email="maria@gmail.com", telefone="11999999999")
    ]

router = APIRouter(
    prefix="/clientes"
)


# Obter todos os clientes
@router.get("/", response_model=list[Cliente])
async def listar_clientes(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)]):
    return await cliente_repositorio.listar_clientes()


# Obter cliente por ID
@router.get("/{cliente_id}", response_model=Cliente | None)
async def obter_cliente(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)], cliente_id: int):

    cliente = await cliente_repositorio.obter_cliente(cliente_id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente


# Criar um cliente
@router.post("/", response_model=Cliente, status_code=201)
async def criar_cliente(
   cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
   cliente: ClienteCriarAtualizar
):
    return await cliente_repositorio.criar_cliente(cliente)


# Atualizar um cliente
@router.put("/{cliente_id}", response_model=Cliente, status_code=201)
async def atualizar_cliente(
   cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
   cliente: ClienteCriarAtualizar,
   cliente_id: int
):
    cliente_atualizado = await cliente_repositorio.atualizar_cliente(cliente, cliente_id)
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente_atualizado


# Deletar um cliente
@router.delete("/{cliente_id}", status_code=204)
async def deletar_cliente(
   cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
   cliente_id: int
):
    sucesso = await cliente_repositorio.deletar_cliente(cliente_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cliente não encontrado") 