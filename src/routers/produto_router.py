from fastapi import APIRouter
from services import produto_service as service
from models.produto import Produto, ProdutoUpdate

routerProduto = APIRouter(prefix="/produto", tags=["Produto"])

@routerProduto.get("/produtoPorNome/{nome}/{limit}/{offset}")
async def ProdutoPorNome(nome:str,limit:int,offset:int):
    return await service.produtosPorNome(nome,limit,offset)

@routerProduto.get("/produtosPorCategoria/{categoria}/{limit}/{offset}")
async def ProdutosPorCategoria(categoria: str,limit:int,offset:int):
    return await service.produtosPorCategoria(categoria,limit,offset)

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
async def deletarProduto(id: str):
    return await service.deletarProduto(id)

@routerProduto.put("/atualizar/{id}")
async def atualizarProduto(id: str,update: ProdutoUpdate):
    return await service.atualizarProduto(id,update)
