from pydantic import BaseModel

class Fornecedor(BaseModel):
    cnpj: int
    nome: str
    contato: str
    endereco: str
    # transacoesFornecedor - lista de transacoes dele
    # produtosFornecedor - lista de produtos dele




