from pydantic import BaseModel
from datetime import datetime;

class Transacao(BaseModel):
    quantidade: int 
    data_transacao: datetime | None
    # Fornecedor dono dessa transacao
    # lista de produtos que ela possui








