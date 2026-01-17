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

@routerProduto.get("/produtosQuantidade")
async def produtosQuantidade():
    return await service.produtosQuantidade()

@routerProduto.get("/produtosPorNomeParcial/{mercadoria}")
async def produtosPorNomeParcial(mercadoria):
    return await service.produtosPorNomeParcial(mercadoria)

@routerProduto.get("/totalVendasDaCategoria/{categoria}")
async def totalVendasDaCategoria(categoria):
    return await service.totalVendasDaCategoria(categoria)


@routerProduto.get("/produtosMaisCaros/{typeSort}/{limit}/{offset}")
async def produtosMaisCaros(typeSort: int,limit: int,offset: int):
    return await service.produtosMaisCaros(typeSort,limit,offset)

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

