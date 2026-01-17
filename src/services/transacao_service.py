import logging
from uuid import UUID

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

        # fornecedor: Fornecedor | None = None

        if data_inicial and not data_final:
            transacao = await Fornecedor.aggregate([
                {'$match': {'_id': fornecedor_id}},
                {
                    '$project': {
                        '_id': 0,
                        'transacoesFornecedor': {
                            '$slice': [
                                {
                                    '$filter': {
                                        'input': '$transacoesFornecedor',
                                        'as': 't',
                                        'cond': {'$gte': ['$$t.data_transacao', data_inicial]}
                                    },
                                },
                                skip,
                                limit
                            ]
                        }
                    }
                }
            ]).to_list()

            if not transacao:
                raise NotFoundException("Não foi encontrar o respectivo fornecedor.")

            return transacao[0]['transacoesFornecedor']

        if not data_inicial and data_final:
            transacao = await Fornecedor.aggregate([
                {'$match': {'_id': fornecedor_id}},
                {
                    '$project': {
                        '_id': 0,
                        'transacoesFornecedor': {
                            '$slice': [
                                {
                                    '$filter': {
                                        'input': '$transacoesFornecedor',
                                        'as': 't',
                                        'cond': {'$lte': ['$$t.data_transacao', data_final]}
                                    },
                                },
                                skip,
                                limit
                            ]
                        }
                    }
                }
            ]).to_list()

            if not transacao:
                raise NotFoundException("Não foi encontrar o respectivo fornecedor.")

            return transacao[0]['transacoesFornecedor']

        if data_inicial and data_final:
            transacao = await Fornecedor.aggregate([
                {'$match': {'_id': fornecedor_id}},
                {
                    '$project': {
                        '_id': 0,
                        'transacoesFornecedor': {
                            '$slice': [
                                {
                                    '$filter': {
                                        'input': '$transacoesFornecedor',
                                        'as': 't',
                                        'cond': {
                                            '$and': [
                                                {'$gte': ['$$t.data_transacao', data_inicial]},
                                                {'$lte': ['$$t.data_transacao', data_final]}
                                            ]
                                        }
                                    },
                                },
                                skip,
                                limit
                            ]
                        }
                    }
                }
            ]).to_list()

            if not transacao:
                raise NotFoundException("Não foi encontrar o respectivo fornecedor.")

            return transacao[0]['transacoesFornecedor']

        fornecedor = await Fornecedor.aggregate([
            {'$match': {'_id': fornecedor_id}},
            {
                '$project': {
                    '_id': 0,
                    'transacoesFornecedor': {
                        '$slice': ['$transacoesFornecedor', skip, limit]
                    }
                }
            }
        ]).to_list()

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        return fornecedor[0]['transacoesFornecedor']

    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao acessar transações",
            exc_info=True
        )
        raise Exception("Erro interno ao acessar transações.")


async def resgatarUm(fornecedor_id: PydanticObjectId, transacao_id: str):
    try:
        fornecedor = await Fornecedor.aggregate([
            {'$match': {'_id': fornecedor_id}},
            {
                '$project': {
                    'transacoesFornecedor': {
                        '$filter': {
                            'input': '$transacoesFornecedor',
                            'as': 't',
                            'cond': {
                                '$eq': ['$$t.id', transacao_id]
                            }
                        }
                    }
                }
            }
        ]).to_list()

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor ou transação com esses respectivos ID's.")

        return fornecedor[0]['transacoesFornecedor']

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
        fornecedor = await Fornecedor.aggregate([
            {'$match': {'_id': fornecedor_id}},
            {'$project': {
                '_id': 1,
                'nome': 1,
                'cnpj': 1,
                'contato': 1,
                'endereco': 1,
                'transacoesFornecedor': {
                    '$slice': ['$transacoesFornecedor', 1, 1]
                }
            }}
        ]).to_list()

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor com esse respectivo ID.")

        await Fornecedor.update(Fornecedor(**fornecedor[0]), {'$push': {'transacoesFornecedor': transacao}})
    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao criar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao criar transação.")


async def atualizar(fornecedor_id: PydanticObjectId, transacao_id: str, transacao: Transacao):
    try:
        fornecedor = await Fornecedor.aggregate([
            {'$match': {'_id': fornecedor_id}},
            {'$project': {
                '_id': 1,
                'nome': 1,
                'cnpj': 1,
                'contato': 1,
                'endereco': 1,
                'transacoesFornecedor': {
                    '$slice': ['$transacoesFornecedor', 1, 1]
                }
            }}
        ]).to_list()

        if not fornecedor:
            raise NotFoundException("O respectivo fornecedor não existe.")

        if not transacao.data_transacao or transacao.quantidade == 0 or not transacao.listaDosProdutos or len(
                transacao.listaDosProdutos) == 0:
            raise BadRequestException("Objeto de atualização incorreto")

        await Fornecedor.update(
            Fornecedor(**fornecedor[0]),
            {
                '$set': {
                    'transacoesFornecedor.$[elem].data_transacao': transacao.data_transacao,
                    'transacoesFornecedor.$[elem].quantidade': transacao.quantidade,
                    'transacoesFornecedor.$[elem].listaDosProdutos': transacao.listaDosProdutos,
                }
            },
            array_filters=[{'elem.id': transacao_id}],
        )
    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao atualizar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao atualizar transação.")


async def deletar(fornecedor_id: PydanticObjectId, transacao_id: str):
    try:
        fornecedor = await Fornecedor.aggregate([
            {'$match': {'_id': fornecedor_id}},
            {'$project': {
                '_id': 1,
                'nome': 1,
                'cnpj': 1,
                'contato': 1,
                'endereco': 1,
                'transacoesFornecedor': {
                    '$slice': ['$transacoesFornecedor', 1, 1]
                }
            }}
        ]).to_list()

        if not fornecedor:
            raise NotFoundException("Não existe fornecedor ou transação com esses respectivos ID's.")

        await Fornecedor.update(Fornecedor(**fornecedor[0]), {'$pull': {'transacoesFornecedor': {'id': transacao_id}}})
    except BusinessException as e:
        raise e

    except Exception as e:
        logger.error(
            "Erro ao deletar uma transação",
            exc_info=True
        )
        raise Exception("Erro interno ao deletar transação.")
