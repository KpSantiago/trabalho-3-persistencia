from datetime import datetime;
from models.produto import Produto
from beanie import Document, Link

class Transacao(Document):
    quantidade: int 
    data_transacao: datetime | None
    listaDosProdutos: list[Link[Produto]] | None

    class Settings:
        name = "transacao"










