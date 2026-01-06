from pydantic import BaseModel
from datetime import datetime;
from models.produto import Produto
import pymongo
from beanie import Document

class Transacao(Document):
    quantidade: int 
    data_transacao: datetime | None
    listaDosProdutos: list[Produto] 

    class Settings:
        name = "transacao"










