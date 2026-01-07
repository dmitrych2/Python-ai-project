import asyncio
from database.db import engine
from database.models import Base

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Таблицы созданы")

# запуск скрипта
if __name__ == "__main__":
    asyncio.run(init())
