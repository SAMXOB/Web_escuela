import sys, asyncio

# Compatibilidad con Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from Apis.config.database import engine
from Apis.models import Base  # ← ahora sí encontrará Base

async def create_tables():
    async with engine.begin() as conn:
        print("🔄 Creando tablas en Neon...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas exitosamente en Neon.")

if __name__ == "__main__":
    asyncio.run(create_tables())
