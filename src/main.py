from fastapi import FastAPI
from routers.produto_router import routerProduto
# from routers.fornecedor_router import routerFornecedor
# from routers.transacao_router import router as routerTransacao


tags_metadata = [
    {
        "name": "Fornecedor",
        "description": "Operações de gerenciamento de fornecedores",
    },
    {
        "name": "Produto",
        "description": "Operações de gerenciamento de produtos",
    },
    {
        "name": "Transação",
        "description": "Operações de gerenciamento de transações",
    },
]

app = FastAPI(
    title="Sistema de Estoque",
    openapi_tags=tags_metadata,
    description="API para gerenciar fornecedores, produtos e transações.",
    version="1.0.0",
)



app.include_router(routerProduto)
# app.include_router(routerFornecedor)
# app.include_router(routerTransacao)