from pydantic import BaseModel
from typing import Optional 
import pymongo
from beanie import Document


class Produto(Document): 
    mercadoria: str
    valor: float
    categoria: str

    class Settings:
        name = "produto"

class ProdutoDto(BaseModel): 
    mercadoria: str
    valor: float
    categoria: str

class ProdutoUpdate(BaseModel):
    mercadoria: Optional[str] = None
    valor: Optional[float] = None
    categoria: Optional[str] = None
    
def produto_serializer(ProdutoDTO: dict) -> Produto:
    produto = Produto(
       mercadoria=ProdutoDTO.mercadoria,
       valor=ProdutoDTO.valor,
       categoria=ProdutoDTO.categoria)

    return produto

def produtoList_serializer(lista) -> list:
    return [produto_serializer(item) for item in lista]
