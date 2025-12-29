import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient 

load_dotenv()

uri = os.getenv("MONGOURL")
client = AsyncIOMotorClient(uri) 
db = client.estoqueDB 

ProductsCollection = db.Produtos 
ProductsFornCollection = db.ProdutoFornecedor 

