import logging
from typing import List

from beanie.odm.fields import PydanticObjectId

from exceptions.bad_request_exception import BadRequestException
from exceptions.business_exception import BusinessException
from exceptions.not_found_exception import NotFoundException
from models.transacao import Transacao
from models.fornecedor import Fornecedor

from datetime import datetime

logger = logging.getLogger(__name__)


async def resgatarTodas(
        fornecedor_id: PydanticObjectId,
        offset: int,
        limit: int,
        data_inicial: datetime | None = None,
        data_final: datetime | None = None,
):
    try:
        skip = (offset - 1) * limit

        fornecedor: Fornecedor | None = None

        if data_inicial and not data_final:
            fornecedor = await Fornecedor.find_one({
                '_id': fornecedor_id,
                'transacoesFornecedor': {
                    'data_transacao': {'$gte': data_inicial}
                }
            })

            return fornecedor.transacoesFornecedor[skip:(skip + limit)]

        if not data_inicial and data_final:
            fornecedor = await Fornecedor.find_one({
                '_id': fornecedor_id,
                'transacoesFornecedor': {
                    'data_transacao': {'$lte': data_inicial}
                }
            })

            return fornecedor.transacoesFornecedor[skip:(skip + limit)]

        if data_inicial and data_final:
            fornecedor = await Fornecedor.find_one({
                '_id': fornecedor_id,
                'transacoesFornecedor': {
                    'data_transacao': {'$in': [data_inicial, data_final]}
                }
            })

            return fornecedor.transacoesFornecedor[skip:(skip + limit)]

        fornecedor = await Fornecedor.find_one({'_id': fornecedor_id})

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

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
        fornecedor = await Fornecedor.find_one({
            '_id': fornecedor_id,
            'transacoesFornecedor': {
                'id': transacao_id
            }
        })

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor ou transação com esses respectivos ID's.")

        return fornecedor.transacoesFornecedor

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
        fornecedor = await Fornecedor.find_one({
            '_id': fornecedor_id,
            'transacoesFornecedor': {
                'id': transacao_id
            }
        })

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor ou transação com esses respectivos ID's.")

        if not transacao.data_transacao or transacao.quantidade == 0 or not transacao.listaDosProdutos or len(
                transacao.listaDosProdutos) == 0:
            raise BadRequestException("Objeto de atualização incorreto")

        t = fornecedor.transacoesFornecedor[0]
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
        fornecedor = await Fornecedor.find_one({
            '_id': fornecedor_id,
            'transacoesFornecedor': {
                'id': transacao_id
            }
        })

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor ou transação com esses respectivos ID's.")

        fornecedor.transacoesFornecedor.remove(fornecedor.transacoesFornecedor[0])
        await fornecedor.save()

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao deletar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao deletar transação.")
