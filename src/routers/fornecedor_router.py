from fastapi import APIRouter, Query
from models.fornecedor import FornecedorDTO, FornecedorUpdate
from services.fornecedor_service import (
    lerFornecedor,
    listarFornecedores,
    cadastrarFornecedor,
    atualizarFornecedor,
    deletarFornecedor,
    buscar_fornecedor_por_nome,
    buscar_fornecedor_por_endereco,
    contar_fornecedores,
    ordenar_fornecedores_por_nome,
    ordenar_fornecedores_por_cnpj,
    listarFornecedoresComProdutos,
    listarFornecedoresPorCategoriaProduto,
)

routerFornecedor = APIRouter(prefix="/fornecedor", tags=["Fornecedores"])

@routerFornecedor.get("/")
async def listar_fornecedores(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return await listarFornecedores(page, page_size)

@routerFornecedor.get("/{id}")
async def ler_fornecedor(id: str):
    return await lerFornecedor(id)

@routerFornecedor.post("")
async def criar_fornecedor(fornecedor: FornecedorDTO):
    return await cadastrarFornecedor(fornecedor)

@routerFornecedor.put("/{id}")
async def atualizar_fornecedor(id: str, fornecedor: FornecedorUpdate):
    return await atualizarFornecedor(id, fornecedor)

@routerFornecedor.delete("/{id}")
async def deletar_fornecedor(id: str):
    return await deletarFornecedor(id)

@routerFornecedor.get("/buscar/nome")
async def buscar_por_nome(nome: str = Query(...), limit: int = Query(20, ge=1), offset: int = Query(0, ge=0)):
    return await buscar_fornecedor_por_nome(nome, limit, offset)

@routerFornecedor.get("/buscar/endereco")
async def buscar_por_endereco(endereco: str = Query(...)):
    return await buscar_fornecedor_por_endereco(endereco)

@routerFornecedor.get("/stats/quantidade")
async def quantidade_fornecedores():
    return await contar_fornecedores()

@routerFornecedor.get("/ordem/nome")
async def ordenacao_por_nome(ordem: str = Query("asc", regex="^(asc|desc)$"), page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return await ordenar_fornecedores_por_nome(ordem, page, page_size)

@routerFornecedor.get("/ordem/cnpj")
async def ordenacao_por_cnpj(ordem: str = Query("asc", regex="^(asc|desc)$")):
    return await ordenar_fornecedores_por_cnpj(ordem)

@routerFornecedor.get("/filtro/com-produtos")
async def listar_com_produtos(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return await listarFornecedoresComProdutos(page, page_size)

@routerFornecedor.get("/filtro/por-categoria")
async def listar_por_categoria(categoria: str = Query(...), page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    return await listarFornecedoresPorCategoriaProduto(categoria, page, page_size)