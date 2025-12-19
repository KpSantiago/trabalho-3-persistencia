from database.database import AsyncSessionLocal

from sqlmodel import select, delete
from sqlalchemy.orm import selectinload

from models.transacao import Transacao
from models.ProdutoTransacaoFornecedor import ProdutoTransacaoFornecedor
from models.produto import Produto

from dtos.transacaoRespostaDTO import TransacaoRespostaDTO, TransacaoProdutoRespostaDTO, TransacaoFornecedorRespostaDTO
from dtos.pagination import Pagination
from dtos.createTransacaoDTO import CreateTransacaoDTO
from dtos.updateTransacaoDTO import UpdateTransacaoDTO

from datetime import datetime

from fastapi import HTTPException

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

async def resgatarTodas(
    offset: int,
    limit: int,
    data_inicial: datetime | None,
    data_final: datetime | None
) -> Pagination[TransacaoRespostaDTO] | str:
    if data_inicial and data_final and data_inicial > data_final:
        return HTTPException(400, "Data inicial não pode ser maior que a data final.")
    
    async with AsyncSessionLocal() as session:
        try:
            statement = select(Transacao)
            if data_inicial and data_final:
                statement = statement.where(
                    Transacao.data_transacao.between(data_inicial, data_final)
                )
            
            statement = (
                statement.offset(offset)
                .limit(limit)
                .options(selectinload(Transacao.itens)
                         .selectinload(ProdutoTransacaoFornecedor.produto),
                         selectinload(Transacao.itens)
                         .selectinload(ProdutoTransacaoFornecedor.fornecedor))
            )

            resultados = await session.exec(statement)
            listaTransacoes = resultados.all()


            todasTransacoes = await session.exec(select(Transacao))
            count = len(todasTransacoes.all())

            resp = Pagination()
            resp.__populate__(offset // limit + 1, limit, count)

            for t in listaTransacoes:
                transacao = TransacaoRespostaDTO(
                    transacao_id=t.transacao_id,
                    quantidade=t.quantidade,
                    data_transacao=t.data_transacao,
                    valor_total=0,
                    produtos=[],
                    fornecedores=[]
                )

                for item in t.itens:
                    transacao.produtos.append(TransacaoProdutoRespostaDTO(
                        produto_id=getattr(item.produto, "idProd", None),
                        mercadoria=getattr(item.produto, "mercadoria", None),
                        categoria=getattr(item.produto, "categoria", None),
                        valor=getattr(item, "valor", None)
                    ))
                    
                    transacao.valor_total = item.valor * item.quantidade
                    
                    transacao.fornecedores.append(TransacaoFornecedorRespostaDTO(
                        fornecedor_id=getattr(item.fornecedor, "idForn", None),
                        nome=getattr(item.fornecedor, "nome", None),
                        cnpj=getattr(item.fornecedor, "cnpj", None),
                    ))

                resp.content.append(transacao)

            return resp

        except Exception as e:
            await session.rollback()
            return f"Error: {e}"

async def resgatarUm(id: int) -> TransacaoRespostaDTO | str:
 async with AsyncSessionLocal() as session:
        try:
            statement = (
                select(Transacao)
                .options(
                selectinload(Transacao.itens).selectinload(ProdutoTransacaoFornecedor.produto),
                selectinload(Transacao.itens).selectinload(ProdutoTransacaoFornecedor.fornecedor)
                )
                .where(Transacao.transacao_id == id)
            )

            result = await session.exec(statement)
            transacao = result.first()

            if not transacao:
                return HTTPException(404, "Transação não encontrada.")

            resp = TransacaoRespostaDTO(
                transacao_id=transacao.transacao_id,
                quantidade=transacao.quantidade,
                data_transacao=transacao.data_transacao,
                valor_total=0,
                produtos=[],
                fornecedores=[]
            )
            
            for item in transacao.itens:
                resp.produtos.append(TransacaoProdutoRespostaDTO(
                    produto_id=getattr(item.produto, "idProd", None) if item.produto else None,
                    mercadoria=getattr(item.produto, "mercadoria", None) if item.produto else None,
                    categoria=getattr(item.produto, "categoria", None) if item.produto else None,
                    valor=item.valor
                ))
                
                if item.valor and item.quantidade:
                    resp.valor_total += item.valor * item.quantidade
                
                if item.fornecedor:
                    resp.fornecedores.append(TransacaoFornecedorRespostaDTO(
                        fornecedor_id=getattr(item.fornecedor, "idForn", None),
                        nome=getattr(item.fornecedor, "nome", None),
                        cnpj=getattr(item.fornecedor, "cnpj", None)
                    ))
                
            return resp
        except Exception as e:
            await session.rollback()
            return(f"Error: {e}")
        
async def criar(transacao: CreateTransacaoDTO) -> str:
    async with AsyncSessionLocal() as session:
        try:
            nova_transacao = Transacao()
            nova_transacao.quantidade = sum(item.quantidade for item in transacao.itens if item.quantidade)
            nova_transacao.data_transacao = datetime.now()
            
            session.add(nova_transacao)
            await session.flush()
            
            for item in transacao.itens:
                p = await session.get(Produto, item.produto_id)
                
                p_t_f = ProdutoTransacaoFornecedor(
                    produto_id=item.produto_id,
                    fornecedor_id=item.fornecedor_id,
                    transacao_id=nova_transacao.transacao_id,
                    quantidade=item.quantidade,
                    valor=p.valor if p else 0.0
                )
                
                p.quantidade += item.quantidade
                await session.flush()
                
                session.add(p_t_f)
                
            await session.commit()
            
            return "Transação criada com sucesso!"
        except Exception as e:
            await session.rollback()
            return(f"Error: {e}")
        
async def atualizar(id: int, transacao: UpdateTransacaoDTO) -> str:
    async with AsyncSessionLocal() as session:
        try:
            transacao_existente = await session.get(Transacao, id)

            if not transacao_existente:
                return HTTPException(404, "Transação não encontrada.")
            
            if len(transacao.itens) > 0:
                transacao_existente.quantidade = sum(item.quantidade for item in transacao.itens if item.quantidade)    
                
                await session.execute(
                    delete(ProdutoTransacaoFornecedor).where(
                        ProdutoTransacaoFornecedor.transacao_id == transacao_existente.transacao_id
                    )
                )
                await session.flush()
                
                for item in transacao.itens:
                    p = await session.get(Produto, item.produto_id)
                    
                    p_t_f = ProdutoTransacaoFornecedor(
                        produto_id=item.produto_id,
                        fornecedor_id=item.fornecedor_id,
                        transacao_id=id,
                        quantidade=item.quantidade,
                        valor=p.valor if p else 0.0
                    )
                    
                    p.quantidade += item.quantidade
                    await session.flush()
                    
                    session.add(p_t_f)
                
            if transacao.data_transacao:
                transacao_existente.data_transacao = transacao.data_transacao
            
            session.add(transacao_existente)
            await session.commit()
            
            return "Transacao atualizada com sucesso."
        except Exception as e:
            await session.rollback()
            return(f"Error: {e}")
        
async def deletar(id: int) -> str:
    async with AsyncSessionLocal() as session:
        try:
            transacao_existente = await session.get(Transacao, id)
            
            if not transacao_existente:
                return HTTPException(404, "Transação não encontrada.")
            
            statement = delete(Transacao).where(Transacao.transacao_id == id)
            
            await session.exec(statement)
            await session.commit()
            
            return "Transação deletada com sucesso."
        except Exception as e:
            await session.rollback()
            return(f"Error: {e}")