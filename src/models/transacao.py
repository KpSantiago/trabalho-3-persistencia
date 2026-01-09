from datetime import datetime;
from models.produto import Produto
from beanie import Document

class Transacao(Document):
    quantidade: int 
    data_transacao: datetime | None
    listaDosProdutos: list[Produto] 

    class Settings:
        name = "transacao"










