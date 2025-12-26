from pydantic import BaseModel
from bson import ObjectId
from typing import Optional 


class Produto(BaseModel): 
    mercadoria: str
    valor: float
    quantidade: int
    categoria: str

class ProdutoUpdate(BaseModel):
    mercadoria: Optional[str] = None
    valor: Optional[float] = None
    quantidade: Optional[int] = None
    categoria: Optional[str] = None
    

