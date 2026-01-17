from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter, Query

from models.transacao import Transacao, CreateTransacao, UpdateTransacao
from services.transacao_service import resgatarTodas, resgatarUm, criar, atualizar, deletar

router = APIRouter(prefix="/fornecedores", tags=["Transação"])


@router.get("/{fornecedor_id}/transacoes")
async def listar_transacoes(
        fornecedor_id: PydanticObjectId,
        offset: int = Query(default=1),
        limit: int = Query(default=10),
        data_inicial: datetime = Query(default=None),
        data_final: datetime = Query(default=None),
):
    """
    Obtém a lista de transações com filtros opcionais de data.

    Args:\n
        fornecedor_id (str): ID da fornecedor
        offset (int): Página (começa em 1)\n
        limit (int): Quantidade de transações por página\n
        data_inicial (datetime): data incial de busca de transações
        data_final (datetime): data final de busca de transações

    Returns:\n
        offset: Página atual\n
        limit: Tamanho da página\n
        total: Quantidade total de transações\n
        data: Lista de transações
    """
    if offset < 1 or limit < 1:
        return "Offset e limit devem ser maiores ou iguais a 0."

    return await resgatarTodas(fornecedor_id, offset, limit)


@router.get("/{fornecedor_id}/transacoes/{transacao_id}")
async def obter_transacao(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId):
    """
    Obtém uma transação específica pelo ID.

    Args:\n
        fornecedor_id (str): ID da fornecedor
        transacao_id (str): ID da transação

    Returns:\n
        transacao_id: ID da transação\n
        quantidade: Quantidade da transação\n
        data_transacao: Data da transação\n
        itens: Lista de itens (produtos/fornecedores) da transação
    """
    return await resgatarUm(fornecedor_id, transacao_id)


@router.post("/{fornecedor_id}/transacoes")
async def criar_transacao(fornecedor_id: PydanticObjectId, novaTransacao: CreateTransacao):
    """
    Cria uma nova transação.

    Args:\n
        quantidade (str): Quantidade transacionada\n
        produtos (list): lista dos produtos envolvidos na transacao\n

    Returns:\n
        Transação criada com sucesso
    """
    transacao: Transacao = Transacao(
        data_transacao=datetime.now(),
        listaDosProdutos=novaTransacao.produtos,
        quantidade=novaTransacao.quantidade,
    )

    return await criar(fornecedor_id, transacao)


@router.put("/{fornecedor_id}/transacoes/{transacao_id}")
async def atualizar_transacao(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId,
                              transacaoAtualizada: UpdateTransacao):
    """
    Atualiza uma transação existente.

    Args:\n
        quantidade (str): Nova quantidade\n
        data_transacao (date): Nova data\n
        produtos (list): Lista de produtos envolvidos na transacao\n

    Returns:\n
        Transação atualizada com sucesso
    """
    transacao: Transacao = Transacao(
        data_transacao=transacaoAtualizada.data_transacao,
        listaDosProdutos=transacaoAtualizada.produtos,
        quantidade=transacaoAtualizada.quantidade,
    )

    return await atualizar(fornecedor_id, transacao_id, transacao)


@router.delete("/{fornecedor_id}/transacoes/{transacao_id}")
async def deletar_transacao(fornecedor_id: PydanticObjectId, transacao_id: PydanticObjectId):
    """
    Deleta uma transação pelo ID.

    Args:\n
        fornecedor_id (str): ID do fornecedor
        transacao_id (str): ID da transação a deletar
    Returns:\n
        Mensagem de sucesso ou erro
    """
    return await deletar(fornecedor_id, transacao_id)
