from pydantic import BaseModel
from models.transacao import Transacao

class Fornecedor(BaseModel):
    cnpj: int
    nome: str
    contato: str
    endereco: str
    transacoesFornecedor: list[Transacao] | None




