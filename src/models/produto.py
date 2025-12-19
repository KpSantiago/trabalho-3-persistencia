from pydantic import BaseModel
from bson import ObjectId

class Produto(BaseModel): 
    mercadoria: str
    valor: float
    quantidade: int
    categoria: str


    

