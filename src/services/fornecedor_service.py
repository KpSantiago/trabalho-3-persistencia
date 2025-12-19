from sqlmodel import select
from sqlalchemy import func
from dtos.createFornecedorDTO import FornecedorDTO
from database.database import AsyncSessionLocal
from models.fornecedor import Fornecedor
from sqlalchemy import delete


async def listarFornecedores(page: int = 1, page_size: int = 10):
    async with AsyncSessionLocal() as session:
        try:
            offset = (page - 1) * page_size
            total_result = await session.exec(select(Fornecedor))
            try:
                total_list = total_result.scalars().all()
            except AttributeError:
                total_list = total_result.all()
            total_count = len(total_list)

            query = (
                select(Fornecedor)
                .offset(offset)
                .limit(page_size)
            )
            res = await session.exec(query)
            try:
                fornecedores = res.scalars().all()
            except AttributeError:
                fornecedores = res.all()

            return {
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "total_pages": (total_count + page_size - 1) // page_size,
                "data": fornecedores
            }
        except Exception as error:
            return f"Error: {error}"


async def buscar_fornecedor_por_nome(nome: str, limit: int = 20, offset: int = 0):
    async with AsyncSessionLocal() as session:
        try:
            query = (
                select(Fornecedor)
                .where(Fornecedor.nome.ilike(f"%{nome}%"))
                .limit(limit)
                .offset(offset)
            )

            res = await session.exec(query)
            try:
                results = res.scalars().all()
            except AttributeError:
                results = res.all()
            return results
        except Exception as error:
            return f"Error: {error}"


async def lerFornecedor(id: int):
    async with AsyncSessionLocal() as session:
        try:
            fornecedor = await session.get(Fornecedor, id)
            if not fornecedor:
                return f"Fornecedor com id {id} não encontrado."

            return fornecedor
        except Exception as error:
            return f"Error: {error}"


async def cadastrarFornecedor(novoFornecedor: FornecedorDTO):
    async with AsyncSessionLocal() as session:
        try:
            new = Fornecedor(**novoFornecedor.model_dump())
            session.add(new)
            await session.commit()
            await session.refresh(new)
            return new
        except Exception as error:
            await session.rollback()
            return f"Error: {error}"


async def atualizarFornecedor(id: int, newData: FornecedorDTO):
    async with AsyncSessionLocal() as session:
        try:
            fornecedor = await session.get(Fornecedor, id)
            if not fornecedor:
                return f"Fornecedor com id {id} não encontrado."

            for chave, valor in newData.model_dump().items():
                setattr(fornecedor, chave, valor)

            session.add(fornecedor)
            await session.commit()
            await session.refresh(fornecedor)

            return fornecedor
        except Exception as error:
            await session.rollback()
            return f"Error: {error}"


async def deletarFornecedor(id: int):
    async with AsyncSessionLocal() as session:
        try:
            deletedFornecedor = delete(Fornecedor).where(Fornecedor.idForn == id)
            await session.exec(deletedFornecedor)
            await session.commit()

            return "Fornecedor deletado com sucesso."
        except Exception as error:
            await session.rollback()
            return f"Error: {error}"


async def contar_fornecedores():
    async with AsyncSessionLocal() as session:
        try:
            query = select(func.sum(1)).select_from(Fornecedor)
            result = await session.exec(query)

            arr = result.all()
            if not arr:
                count = 0
            else:
                first = arr[0]
                count = first[0] if isinstance(first, (list, tuple)) else first

            return count or 0
        except Exception as error:
            return f"Error: {error}"


async def ordenar_fornecedores_por_nome():
    async with AsyncSessionLocal() as session:
        try:
            query = select(Fornecedor).order_by(Fornecedor.nome)
            result = await session.exec(query)

            try:
                fornecedores = result.scalars().all()
            except AttributeError:
                fornecedores = result.all()

            return fornecedores
        except Exception as error:
            return f"Error: {error}"
