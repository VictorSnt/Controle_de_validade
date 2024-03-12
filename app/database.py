from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Detalhe
from sqlalchemy import select, text
import os

# Configuração para o banco de dados PostgreSQL alterdata
POSTGRES_DATABASE_URL = f"postgresql+asyncpg://{os.environ['USER_ALTERDATA']}:{os.environ['PASSWD_ALTERDATA']}@{os.environ['HOST_ALTERDATA']}:{os.environ['PORT_ALTERDATA']}/{os.environ['DBNAME_ALTERDATA']}"

# Cria o mecanismo de banco de dados para o PostgreSQL alterdata
alterdata_engine = create_async_engine(
    POSTGRES_DATABASE_URL,
    echo=False
)

# Cria uma sessão baseada no mecanismo de banco de dados PostgreSQL
AlterdataSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=alterdata_engine, class_=AsyncSession)

# Configura o search_path após a conexão ser estabelecida
async def configure_search_path(session):
    try:
        await session.execute(text("SET search_path TO wshop"))
        await session.commit()
    except Exception as e:
        print("Erro ao configurar search_path:", e)

# Use a função configure_search_path para configurar o search_path na sessão
async def main():
    async with AlterdataSessionLocal() as session:
        await configure_search_path(session)
        
        # Executa a consulta para buscar todos os detalhes
        statement = select(Detalhe).limit(15)
        result = await session.execute(statement)
        
        # Coleta os resultados
        detalhes = result.scalars().all()
        
        # Imprime os detalhes
        for detalhe in detalhes:
            print(detalhe)

# Execute o loop principal do asyncio
import asyncio
asyncio.run(main())
