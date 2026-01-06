from pydantic import BaseModel
from typing import Optional 
import pymongo
from beanie import Document

class ProdutoFornecedor(Document):
    produto_id: str 
    fornecedor_id: str 

    class Settings:
        name = "produtoFornecedor"

class ProdutoFornecedorUpdate(BaseModel):
    produto_id: Optional[str] = None
    fornecedor_id: Optional[str] = None










