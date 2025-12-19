from fastapi import APIRouter, Query

from dtos.createTransacaoDTO import CreateTransacaoDTO
from dtos.updateTransacaoDTO import UpdateTransacaoDTO
from dtos.transacaoRespostaDTO import TransacaoRespostaDTO
from dtos.pagination import Pagination 

from services.transacao_service import resgatarTodas, resgatarUm, criar, atualizar, deletar

from datetime import datetime

router = APIRouter(prefix="/transacao", tags=["Transação"])

@router.get("/")
async def listar_transacoes(offset: int = Query(default=1), limit: int = Query(default=10), data_inicial: datetime | None = Query(default=None), data_final: datetime | None = Query(default=None)) -> Pagination[TransacaoRespostaDTO] | str:
    """
    Obtém a lista de transações com filtros opcionais de data.

    Args:\n
        offset (int): Página (começa em 1)\n
        limit (int): Quantidade de transações por página\n
        data_inicial (datetime): Data inicial para filtrar (opcional)\n
        data_final (datetime): Data final para filtrar (opcional)

    Returns:\n
        offset: Página atual\n
        limit: Tamanho da página\n
        total: Quantidade total de transações\n
        data: Lista de transações
    """
    if offset < 1 or limit < 1:
        return await "Offset e limit devem ser maiores ou iguais a 0."
    
    offset = (offset - 1) * limit
    
    return await resgatarTodas(offset, limit, data_inicial, data_final)

@router.get("/{id}")
async def obter_transacao(id: int):
    """
    Obtém uma transação específica pelo ID.

    Args:\n
        id (int): ID da transação

    Returns:\n
        transacao_id: ID da transação\n
        quantidade: Quantidade da transação\n
        data_transacao: Data da transação\n
        itens: Lista de itens (produtos/fornecedores) da transação
    """
    return await resgatarUm(id)

@router.post("/")
async def criar_transacao(novaTransacao: CreateTransacaoDTO):
    """
    Cria uma nova transação.

    Args:\n
        quantidade (int): Quantidade transacionada\n
        data_transacao (date): Data da transação

    Returns:\n
        Transação criada com sucesso
    """
    return await criar(novaTransacao)

@router.put("/{id}")
async def atualizar_transacao(id: int, transacaoAtualizada: UpdateTransacaoDTO):
    """
    Atualiza uma transação existente.

    Args:\n
        id (int): ID da transação\n
        quantidade (int): Nova quantidade (opcional)\n
        data_transacao (date): Nova data (opcional)

    Returns:\n
        Transação atualizada com sucesso
    """
    return await atualizar(id, transacaoAtualizada)

@router.delete("/{id}")
async def deletar_transacao(id: int):
    """
    Deleta uma transação pelo ID.

    Args:\n
        id (int): ID da transação a deletar

    Returns:\n
        Mensagem de sucesso ou erro
    """
    return await deletar(id)