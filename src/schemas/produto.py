
def produto_individual(produto) -> dict:
    return {
        "id": str(produto["_id"]),
        "mercadoria": produto["mercadoria"],
        "valor": produto["valor"],
        "quantidade": produto["quantidade"],
        "categoria": produto["categoria"],
    }