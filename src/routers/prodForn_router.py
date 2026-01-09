
from fastapi import APIRouter
from services import produtoFornecedor_service as service
from models.produtoFornecedor import ProdutoFornecedorUpdate, ProdutoFornecedorDTO

routerProdForn = APIRouter(prefix="/ProdForn", tags=["ProdForn"])


@routerProdForn.post("/cadastrar")
async def cadastrarProdForn(novoProdForn: ProdutoFornecedorDTO):
    return await service.cadastrarProdForn(novoProdForn)

@routerProdForn.delete("/deletar/{id}")
async def deletarProdForn(id: str):
    return await service.deletarProdForn(id)

@routerProdForn.put("/atualizar/{id}")
async def atualizarProdForn(id: str,update: ProdutoFornecedorUpdate):
    return await service.atualizarProdForn(id,update)

