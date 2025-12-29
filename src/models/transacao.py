from pydantic import BaseModel
from datetime import datetime;

class Transacao(BaseModel):
    quantidade: int 
    data_transacao: datetime | None
    listaDosProdutos: list[str] # lista de string, pois essa lista ira armazenas os ID's dos produtos










