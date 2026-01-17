from models.transacao import Transacao
from beanie import Document

class Fornecedor(Document):
    cnpj: int
    nome: str
    contato: str
    endereco: str
    transacoesFornecedor: list[Transacao] | None

    class Settings:
        name = "fornecedor"




