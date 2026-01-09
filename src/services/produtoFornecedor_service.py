
from models.produtoFornecedor import ProdutoFornecedor, ProdutoFornecedorUpdate, ProdutoFornecedorDTO
from beanie.odm.fields import PydanticObjectId


async def cadastrarProdForn(novoProdForn: ProdutoFornecedorDTO):
    try:
        newProdForn = ProdutoFornecedor(produto_id=novoProdForn.produto_id,fornecedor_id=novoProdForn.fornecedor_id)
        await newProdForn.insert()
    except:
        return "Nao foi possivel cadastrar a relacao."

    return novoProdForn


async def deletarProdForn(id):
    try:
        relacao = await ProdutoFornecedor.find_one(ProdutoFornecedor.id == id)

        
        if(relacao):
            return "Relacao excluida com sucesso"
        
        raise ValueError("A relacao nao existe.")
    
    except ValueError as e:
        return e.args[0]


async def atualizarProdForn(id: PydanticObjectId,update: ProdutoFornecedorUpdate):
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


        relacao = await ProdutoFornecedor.find_one(ProdutoFornecedor.id == id)
        await relacao.set(update_filds)

    
        return relacao


    except ValueError as e:
        return e.args[0]