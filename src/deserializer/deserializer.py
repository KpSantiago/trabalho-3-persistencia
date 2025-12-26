from bson import ObjectId

def produto_serializer(produto: dict) -> dict:
    produto["_id"] = str(produto["_id"])
    return produto

def produtoList_serializer(lista) -> list:
    return [produto_serializer(item) for item in lista]