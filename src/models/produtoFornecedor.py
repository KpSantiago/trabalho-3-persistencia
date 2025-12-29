from pydantic import BaseModel
from typing import Optional 

class ProdutoFornecedor(BaseModel):
    produto_id: str 
    fornecedor_id: str 

class ProdutoFornecedorUpdate(BaseModel):
    produto_id: Optional[str] = None
    fornecedor_id: Optional[str] = None










