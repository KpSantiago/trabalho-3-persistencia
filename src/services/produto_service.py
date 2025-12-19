
from database.database import ProductsCollection
from models.produto import Produto
from schemas.produto import produto_individual

async def produtoPorId():
    print()


async def visualizarProdutos():
    produto = await ProductsCollection.find_one({"mercadoria": "string"})
    # print(produto)
    teste = produto_individual(produto)
    return teste


async def cadastrarProduto(novoProduto: Produto):
    await ProductsCollection.insert_one(dict(novoProduto))
    return 1


async def deletarProduto():
    print()


async def atualizarProduto():
    print()


async def fornecedoresDeProdutos():
    print()


async def ProdutosDataTransacoes():
    print()





































        