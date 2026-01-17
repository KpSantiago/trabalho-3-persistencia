from contextlib import asynccontextmanager
from datetime import datetime
from urllib.request import Request

from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from database.database import initDB
from exceptions.business_exception import BusinessException
from routers.prodForn_router import routerProdForn
from routers.produto_router import routerProduto
from routers.transacao_router import router as routerTransacao
from routers.fornecedor_router import routerFornecedor

tags_metadata = [
    {
        "name": "Fornecedores",
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initDB()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Sistema de Estoque",
    openapi_tags=tags_metadata,
    description="API para gerenciar fornecedores, produtos e transações.",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def business_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, BusinessException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": exc.status_code,
                "message": exc.message[0],
                "timestamp": datetime.now().isoformat(),
            })

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(exc),
            "timestamp": datetime.now().isoformat(),
        })


app.include_router(routerProduto)
app.include_router(routerProdForn)
app.include_router(routerTransacao)
app.include_router(routerFornecedor)
