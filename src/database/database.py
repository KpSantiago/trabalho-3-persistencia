import os
from dotenv import load_dotenv
# from motor.motor_asyncio import AsyncIOMotorClient 

from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.produto import Produto
from models.fornecedor import Fornecedor
from models.produtoFornecedor import ProdutoFornecedor



async def initDB():
    load_dotenv()

    uri = os.getenv("MONGOURL")

    client = AsyncMongoClient(uri)
    await init_beanie(database=client.dbTeste, document_models=[Produto,Fornecedor,ProdutoFornecedor])

