from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def close(self) -> None:
        await self.session.close()

    async def add(self, obj) -> None:
        self.session.add(obj)

    async def delete(self, obj) -> None:
        await self.session.delete(obj)

    async def execute_query(self, query):
        return await self.session.execute(query)
