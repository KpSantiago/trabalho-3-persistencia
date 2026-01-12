from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(extra="forbid")

class ProdutoUpdate(BaseModel):
    mercadoria: str | None = None
    valor: float | None = None
    categoria: str | None = None

    model_config = ConfigDict(extra="forbid")

    
def produto_serializer(ProdutoDTO: dict) -> Produto:
    produto = Produto(
       mercadoria=ProdutoDTO["mercadoria"],
       valor=ProdutoDTO["valor"],
       categoria=ProdutoDTO["categoria"])

    return produto

def produtoList_serializer(lista) -> list:
    return [produto_serializer(item) for item in lista]
