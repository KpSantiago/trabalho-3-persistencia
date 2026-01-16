import logging

from beanie.odm.fields import PydanticObjectId

from exceptions.bad_request_exception import BadRequestException
from exceptions.business_exception import BusinessException
from exceptions.not_found_exception import NotFoundException
from models.transacao import Transacao
from models.fornecedor import Fornecedor

logger = logging.getLogger(__name__)


async def resgatarTodas(
        fornecedor_id: PydanticObjectId,
        offset: int,
        limit: int
):
    try:
        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        skip = (offset - 1) * limit
        return fornecedor.transacoesFornecedor[skip:(skip + limit)]

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao acessar transações",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar transações.")


async def resgatarUm(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId):
    try:
        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        transacao = next((t for t in fornecedor.transacoesFornecedor if t.id == transacao_id), None)

        if not transacao:
            raise NotFoundException("Não existe Transação com esse respectivo ID.")

        return transacao

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao acessar transações",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar transações.")


async def criar(fornecedor_id: PydanticObjectId, transacao: Transacao):
    try:
        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        if not fornecedor.transacoesFornecedor:
            fornecedor.transacoesFornecedor = []

        fornecedor.transacoesFornecedor.append(transacao)
        await fornecedor.save()

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao criar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao criar transação.")


async def atualizar(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId, transacao: Transacao):
    try:
        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        t = next((t for t in fornecedor.transacoesFornecedor if t.id == transacao_id), None)

        if not t:
            raise NotFoundException("Não existe transação com esse respectivo ID.")

        if not transacao.data_transacao or transacao.quantidade == 0 or not transacao.listaDosProdutos or len(transacao.listaDosProdutos) == 0:
            raise BadRequestException("Objeto de atualização incorreto")

        t.data_transacao = transacao.data_transacao
        t.quantidade = transacao.quantidade
        t.listaDosProdutos = transacao.listaDosProdutos

        await fornecedor.save()

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao atualizar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao atualizar transação.")


async def deletar(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId):
    try:
        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        transacao = next((t for t in fornecedor.transacoesFornecedor if t.id == transacao_id), None)

        if not transacao:
            raise NotFoundException("Não existe Transação com esse respectivo ID.")

        fornecedor.transacoesFornecedor.remove(transacao)
        await fornecedor.save()

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao deletar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao deletar transação.")
