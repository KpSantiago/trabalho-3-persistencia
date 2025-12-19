from fastapi import APIRouter
from services.fornecedor_service import (
    lerFornecedor,
    listarFornecedores,
    cadastrarFornecedor,
    atualizarFornecedor,
    deletarFornecedor,
    buscar_fornecedor_por_nome,
    contar_fornecedores,
    ordenar_fornecedores_por_nome
)

routerFornecedor = APIRouter(prefix="/fornecedor", tags=["Fornecedor"])

@routerFornecedor.get("/")
async def listar_fornecedores():
    return await listarFornecedores()

@routerFornecedor.get("/quantidade")
async def quantidade_fornecedores():
    return await contar_fornecedores()

@routerFornecedor.get("/ordenacao")
async def ordenacao_fornecedores():
    return await ordenar_fornecedores_por_nome()

@routerFornecedor.get("/buscar")
async def buscar_por_nome():
    return await buscar_fornecedor_por_nome()

@routerFornecedor.get("/{id}")
async def ler_fornecedor(id: int):
    return await lerFornecedor(id)

@routerFornecedor.post("")
async def criar_fornecedor():
    return await cadastrarFornecedor()

@routerFornecedor.put("/{id}")
async def atualizar_fornecedor():
    return await atualizarFornecedor()

@routerFornecedor.delete("/{id}")
async def deletar_fornecedor():
    return await deletarFornecedor(id)
