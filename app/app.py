from sqlalchemy import select
from database import AlterdataSessionLocal
from models import Detalhe

async def fetch_detalhes():
    async with AlterdataSessionLocal() as session:
        async with session.begin():
            # Executa a consulta para buscar todos os detalhes
            statement = select(Detalhe).limit(10)
            result = await session.execute(statement)

            # Coleta os resultados
            detalhes = result.scalars().all()

            return detalhes

# Exemplo de uso:
async def main():
    detalhes = await fetch_detalhes()
    for detalhe in detalhes:
        print(detalhe)

# Executar o loop principal do asyncio
import asyncio
asyncio.run(main())
