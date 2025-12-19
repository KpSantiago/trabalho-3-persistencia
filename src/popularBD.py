import asyncio
from datetime import datetime
from database.database import AsyncSessionLocal, create_db_and_tables
from models.produto import Produto
from models.fornecedor import Fornecedor
from models.ProdutoTransacaoFornecedor import ProdutoTransacaoFornecedor
from models.transacao import Transacao

from datetime import datetime


async def popular_banco():
    # Criar tabelas se não existirem
    await create_db_and_tables()

    async with AsyncSessionLocal() as session:
        # -----------------------
        # 10 FORNECEDORES
        # -----------------------
        fornecedores = [
            Fornecedor(idForn=1, cnpj=11111111111111, nome="Fornecedor A", contato="contatoA@gmail.com", endereco="Rua A, 100"),
            Fornecedor(idForn=2, cnpj=22222222222222, nome="Fornecedor B", contato="contatoB@gmail.com", endereco="Rua B, 200"),
            Fornecedor(idForn=3, cnpj=33333333333333, nome="Fornecedor C", contato="contatoC@gmail.com", endereco="Rua C, 300"),
            Fornecedor(idForn=4, cnpj=44444444444444, nome="Fornecedor D", contato="contatoD@gmail.com", endereco="Rua D, 400"),
            Fornecedor(idForn=5, cnpj=55555555555555, nome="Fornecedor E", contato="contatoE@gmail.com", endereco="Rua E, 500"),
            Fornecedor(idForn=6, cnpj=66666666666666, nome="Fornecedor F", contato="contatoF@gmail.com", endereco="Rua F, 600"),
            Fornecedor(idForn=7, cnpj=77777777777777, nome="Fornecedor G", contato="contatoG@gmail.com", endereco="Rua G, 700"),
            Fornecedor(idForn=8, cnpj=88888888888888, nome="Fornecedor H", contato="contatoH@gmail.com", endereco="Rua H, 800"),
            Fornecedor(idForn=9, cnpj=99999999999999, nome="Fornecedor I", contato="contatoI@gmail.com", endereco="Rua I, 900"),
            Fornecedor(idForn=10, cnpj=10101010101010, nome="Fornecedor J", contato="contatoJ@gmail.com", endereco="Rua J, 1000"),
        ]

        session.add_all(fornecedores)

        # -----------------------
        # 10 PRODUTOS
        # -----------------------
        produtos = [
            Produto(idProd=1, mercadoria="Arroz", valor=20.50, quantidade=100, categoria="Alimento"),
            Produto(idProd=2, mercadoria="Feijão", valor=10.0, quantidade=150, categoria="Alimento"),
            Produto(idProd=3, mercadoria="Macarrão", valor=7.8, quantidade=200, categoria="Alimento"),
            Produto(idProd=4, mercadoria="Óleo", valor=6.5, quantidade=180, categoria="Alimento"),
            Produto(idProd=5, mercadoria="Açúcar", valor=5.2, quantidade=140, categoria="Alimento"),
            Produto(idProd=6, mercadoria="Sabonete", valor=2.5, quantidade=300, categoria="Higiene"),
            Produto(idProd=7, mercadoria="Detergente", valor=3.0, quantidade=250, categoria="Limpeza"),
            Produto(idProd=8, mercadoria="Shampoo", valor=12.0, quantidade=120, categoria="Higiene"),
            Produto(idProd=9, mercadoria="Café", valor=15.0, quantidade=90, categoria="Alimento"),
            Produto(idProd=10, mercadoria="Sal", valor=2.0, quantidade=500, categoria="Alimento"),
        ]

        session.add_all(produtos)



        # -----------------------
        # TRANSACOES
        # -----------------------
        transacoes = [
            Transacao(tipo=1, quantidade=50, data_transacao=datetime.fromisoformat("2025-01-01")),
            Transacao(tipo=1, quantidade=70, data_transacao=datetime.fromisoformat("2025-01-02")),
            Transacao(tipo=0, quantidade=20, data_transacao=datetime.fromisoformat("2025-01-03")),
            Transacao(tipo=1, quantidade=40, data_transacao=datetime.fromisoformat("2025-01-04")),
            Transacao(tipo=0, quantidade=10, data_transacao=datetime.fromisoformat("2025-01-05")),
            Transacao(tipo=1, quantidade=100, data_transacao=datetime.fromisoformat("2025-01-06")),
            Transacao(tipo=1, quantidade=60, data_transacao=datetime.fromisoformat("2025-01-07")),
            Transacao(tipo=0, quantidade=30, data_transacao=datetime.fromisoformat("2025-01-08")),
            Transacao(tipo=1, quantidade=80, data_transacao=datetime.fromisoformat("2025-01-09")),
            Transacao(tipo=0, quantidade=25, data_transacao=datetime.fromisoformat("2025-01-10")),
        ]

        session.add_all(transacoes)

        # -----------------------
        # ProdutoTransacaoFornecedor
        # -----------------------

        ptf = [
            ProdutoTransacaoFornecedor(produto_id=1, fornecedor_id=1, transacao_id=1, quantidade=25, valor=20.50),
            ProdutoTransacaoFornecedor(produto_id=2, fornecedor_id=1, transacao_id=2, quantidade=25, valor=10.0),
            ProdutoTransacaoFornecedor(produto_id=3, fornecedor_id=2, transacao_id=3, quantidade=25, valor=7.8),
            ProdutoTransacaoFornecedor(produto_id=4, fornecedor_id=2, transacao_id=4, quantidade=25, valor=6.5),
            ProdutoTransacaoFornecedor(produto_id=5, fornecedor_id=3, transacao_id=5, quantidade=25, valor=5.2),
            ProdutoTransacaoFornecedor(produto_id=6, fornecedor_id=4, transacao_id=6, quantidade=25, valor=2.5),
            ProdutoTransacaoFornecedor(produto_id=7, fornecedor_id=5, transacao_id=7, quantidade=25, valor=3.0),
            ProdutoTransacaoFornecedor(produto_id=8, fornecedor_id=6, transacao_id=8, quantidade=25, valor=12.0),
            ProdutoTransacaoFornecedor(produto_id=9, fornecedor_id=7, transacao_id=9, quantidade=25, valor=15.0),
            ProdutoTransacaoFornecedor(produto_id=10, fornecedor_id=8, transacao_id=10, quantidade=25, valor=2.0),
        ]

        session.add_all(ptf)

        # SALVA TUDO
        await session.commit()

        print("Banco populado com sucesso!")


if __name__ == "__main__":
    asyncio.run(popular_banco())