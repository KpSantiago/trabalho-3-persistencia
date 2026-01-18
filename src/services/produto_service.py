import logging

from beanie.odm.fields import PydanticObjectId

from exceptions.bad_request_exception import BadRequestException
from exceptions.business_exception import BusinessException
from exceptions.not_found_exception import NotFoundException
from models.produto import Produto, ProdutoDto, ProdutoUpdate, produtoList_serializer
from services.fornecedor_service import listarFornecedoresComProdutos
from datetime import datetime,date

logger = logging.getLogger(__name__)


async def produtosPorNome(nome, limit, offset):
    try:
        produtosLista = await Produto.find(Produto.mercadoria == nome).skip(offset).limit(limit).to_list()

        return produtosLista
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def produtosTransacionadosPorData(dataInicio: datetime, dataFim: datetime):
    try:
        dataInicio = datetime.fromisoformat(dataInicio)
        dataFim = datetime.fromisoformat(dataFim)

        fornecedores = await listarFornecedoresComProdutos()

        produtosList = []

        for forn in fornecedores:
            for tran in forn["transacoesFornecedor"]:
                if(tran["data_transacao"] > dataInicio and tran["data_transacao"] < dataFim):
                    produtosList[len(produtosList):] = tran["listaDosProdutos"]
        

        return produtosList
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def produtosPorNomeParcial(mercadoria):
    try:
        pipeLine = [
            {
                "$project": {"_id": 0}
            },
            {
                "$match": {"mercadoria": {"$regex": mercadoria, "$options": "i"}}
            }
        ]

        return await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def produtosPorCategoria(categoria, limit, offset):
    try:
        produtosLista = await Produto.find(Produto.categoria == categoria).skip(offset).limit(limit).to_list()

        return produtosLista

    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def produtosQuantidade():
    try:
        qtdProdutos = await Produto.count()

        return qtdProdutos
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def totalVendasDaCategoria(categoria):
    try:
        pipeLine = [
            {
                "$match": {"categoria": {"$regex": categoria, "$options": "i"}}
            },

            {
                "$group": {
                    "_id": "$categoria",
                    "totalVendas": {"$sum": "$valor"}
                }
            }
        ]

        return await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def produtosPorPreco(typeSort, limit, offset):
    try:
        pipeLine = [
            {
                "$project": {"_id": 0}
            },
            {
                "$sort": {
                    "valor": typeSort

                }
            },
            {
                "$limit": limit
            },
            {
                "$skip": offset
            }
        ]

        return await Produto.aggregate(pipeLine).to_list()
    except Exception:
        logger.error(
            "Erro ao acessar produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar produtos.")


async def cadastrarProduto(novoProduto: ProdutoDto):
    try:
        newP = Produto(
            mercadoria=novoProduto.mercadoria,
            valor=novoProduto.valor,
            categoria=novoProduto.categoria)
        await newP.insert()

        return newP

    except Exception:
        logger.error(
            "Erro ao cadastra produto.",
            exc_info=True
        )
        raise Exception("Erro interno ao cadastrar produto.")


async def cadastrarMuitosProduto(listaNovosProdutosDTO: list[ProdutoDto]):
    try:
        ListaNovosProdutos = produtoList_serializer(listaNovosProdutosDTO)
        await Produto.insert_many(ListaNovosProdutos)

        return listaNovosProdutosDTO
    except Exception:
        logger.error(
            "Erro ao cadastrar muitos produtos",
            exc_info=True
        )
        raise Exception("Erro interno ao cadastrar muitos produtos.")


async def deletarProduto(id: PydanticObjectId):
    try:
        produto = await Produto.find_one(Produto.id == id)

        if (produto):
            await produto.delete()
            return "Produto excluido com sucesso"

        if not produto:
            raise NotFoundException("Produto inexistente")

    except BusinessException as e:
        raise e

    except Exception:
        logger.error(
            "Erro ao deletar produto",
            exc_info=True
        )
        raise Exception("Erro interno ao deletera produto.")


async def atualizarProduto(id, update: ProdutoUpdate):
    try:
        if update.categoria is None and update.mercadoria is None and update.valor is None:
            raise BadRequestException("Modelo de requisiçao invalido.")

        chavesRequest = dict(update).keys()

        update_filds = dict(update)
        for key in chavesRequest:
            if (update_filds[key] == None):
                del update_filds[key]

        produto = await Produto.find_one(Produto.id == id)
        await produto.set(update_filds)

        return produto

    except BusinessException as e:
        raise e

    except Exception:
        logger.error(
            "Erro ao atualizar produto",
            exc_info=True
        )

        raise Exception("Erro interno ao atualizar produto.")
