from fastapi import APIRouter
from services import produto_service as service
from models.produto import ProdutoDto, ProdutoUpdate
from beanie.odm.fields import PydanticObjectId

routerProduto = APIRouter(prefix="/produto", tags=["Produto"])

@routerProduto.get("/produtoPorNome/{nome}/{limit}/{offset}")
async def ProdutoPorNome(nome:str,limit:int,offset:int):
    return await service.produtosPorNome(nome,limit,offset)

@routerProduto.get("/produtosPorCategoria/{categoria}/{limit}/{offset}")
async def ProdutosPorCategoria(categoria: str,limit:int,offset:int):
    return await service.produtosPorCategoria(categoria,limit,offset)

@routerProduto.post("/cadastrar")
async def cadastrarProduto(novoProduto: ProdutoDto):
    return await service.cadastrarProduto(novoProduto)

@routerProduto.post("/cadastrarMuitos")
async def cadastrarMuitosProduto(listaNovosProdutos: list[ProdutoDto]):
    return await service.cadastrarMuitosProduto(listaNovosProdutos)

@routerProduto.delete("/deletar/{id}")
async def deletarProduto(id: PydanticObjectId):
    return await service.deletarProduto(id)

@routerProduto.put("/atualizar/{id}")
async def atualizarProduto(id: PydanticObjectId,update: ProdutoUpdate):
    return await service.atualizarProduto(id,update)

