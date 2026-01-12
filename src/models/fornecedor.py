from models.transacao import Transacao
from beanie import Document, Link

class Fornecedor(Document):
    cnpj: int
    nome: str
    contato: str
    endereco: str
    transacoesFornecedor: list[Link[Transacao]] | None

    class Settings:
        name = "fornecedor"




