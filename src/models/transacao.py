from pydantic import BaseModel
from datetime import datetime;
from models.produto import Produto

class Transacao(BaseModel):
    quantidade: int 
    data_transacao: datetime | None
    listaDosProdutos: list[Produto] 










