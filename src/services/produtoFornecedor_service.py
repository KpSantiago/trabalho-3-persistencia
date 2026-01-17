import logging

from beanie.odm.fields import PydanticObjectId

from exceptions.bad_request_exception import BadRequestException
from exceptions.business_exception import BusinessException
from exceptions.not_found_exception import NotFoundException
from models.produtoFornecedor import ProdutoFornecedor, ProdutoFornecedorUpdate, ProdutoFornecedorDTO

logger = logging.getLogger(__name__)


async def cadastrarProdForn(novoProdForn: ProdutoFornecedorDTO):
    try:
        newProdForn = ProdutoFornecedor(produto_id=novoProdForn.produto_id, fornecedor_id=novoProdForn.fornecedor_id)
        await newProdForn.insert()

        return novoProdForn

    except Exception:
        logger.error(
            "Erro ao acessar cadastrar uma nova relação produto-fornecedor",
            exc_info=True
        )
        raise Exception("Erro interno ao cadastrar uma nova relação produto-fornecedor.")


async def deletarProdForn(id):
    try:
        relacao = await ProdutoFornecedor.find_one(ProdutoFornecedor.id == id)

        if (relacao):
            return "Relacao excluida com sucesso"

        raise NotFoundException("A relação produto-fornecedor não existe.")

    except BusinessException as e:
        raise e

    except Exception:
        logger.error(
            "Erro ao deletar relação produto-fornecedor.",
            exc_info=True
        )
        raise Exception("Erro interno ao deletar relação produto-fornecedor.")


async def atualizarProdForn(id: PydanticObjectId, update: ProdutoFornecedorUpdate):
    try:
        i = 0
        chavesClasse = list(ProdutoFornecedorUpdate.model_fields.keys())
        chavesRequest = dict(update).keys()

        for key in chavesRequest:
            if key != chavesClasse[i]:
                raise BadRequestException(message="Modelo de requisicao invalida.")
            i += 1

        update_filds = dict(update)
        for key in chavesRequest:
            if (update_filds[key] == None):
                del update_filds[key]

        relacao = await ProdutoFornecedor.find_one(ProdutoFornecedor.id == id)
        await relacao.set(update_filds)

        return relacao

    except BusinessException as e:
        raise e

    except Exception:
        logger.error(
            "Erro ao atualizar a relação produto-forncedor",
            exc_info=True
        )
        raise Exception("Erro interno ao atualizar a relação produto-fornecedor.")
