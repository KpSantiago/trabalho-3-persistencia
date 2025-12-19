from fastapi import APIRouter
from services import produto_service as service
from models.produto import Produto

routerProduto = APIRouter(prefix="/produto", tags=["Produto"])

@routerProduto.get("/ProdutoPorId/{id}")
async def produtoPorId():
    return await service.produtoPorId()

@routerProduto.get("/visualizar/{offset}/{qtd}")
async def visualizarProduto():
    return await service.visualizarProdutos()

@routerProduto.get("/fornecedoresDeProdutos/{id}")
async def fornecedoresDeProdutos():
    return await service.fornecedoresDeProdutos()

@routerProduto.get("/produtosDataTransacoes")
async def atualizarProduto():
    return await service.ProdutosDataTransacoes()

@routerProduto.post("/cadastrar")
async def cadastrarProduto(novoProduto: Produto):
    return await service.cadastrarProduto(novoProduto)

@routerProduto.delete("/deletar/{id}")
async def deletarProduto():
    return await service.deletarProduto(id)

@routerProduto.put("/atualizar/{id}")
async def atualizarProduto():
    return await service.atualizarProduto()
