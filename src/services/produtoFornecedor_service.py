
from database.database import ProductsFornCollection
from models.produtoFornecedor import ProdutoFornecedor, ProdutoFornecedorUpdate
from bson import ObjectId


async def cadastrarProdForn(novoProdForn: ProdutoFornecedor):
    try:
        await ProductsFornCollection.insert_one(dict(novoProdForn))
    except:
        return "Nao foi possivel cadastrar a relacao."

    return novoProdForn


async def deletarProdForn(id):
    try:
        query_filter = { "_id": ObjectId(id) }
        result = await ProductsFornCollection.delete_one(query_filter)
        
        if(result.deleted_count != 0):
            return "Relacao excluida com sucesso"
        
        raise ValueError("A relacao nao existe.")
    
    except ValueError as e:
        return e.args[0]


async def atualizarProdForn(id,update: ProdutoFornecedorUpdate):
    try:
        i = 0
        chavesClasse = list(ProdutoFornecedorUpdate.model_fields.keys())
        chavesRequest = dict(update).keys()

        for key in chavesRequest:
            if key != chavesClasse[i]:
                raise ValueError("Modelo de requisicao invalida.")
            i += 1

        update_filds = dict(update)
        for key in chavesRequest:
            if(update_filds[key] == None):
                del update_filds[key]


        query_filter = { "_id": ObjectId(id) }
        update_obj = {"$set": update_filds}

        result = await ProductsFornCollection.update_one(query_filter, update_obj)

    
        return 1


    except ValueError as e:
        return e.args[0]