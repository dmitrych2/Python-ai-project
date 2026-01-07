from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import ChatRequest

async def get_user_request(
        ip_address: str,
        session: AsyncSession
        ):
    query = select(ChatRequest).where(ChatRequest.ip_address==ip_address)
    result = await session.execute(query)
    return result.scalars().first()

async def add_request_data(
        ip_address: str,
        prompt: str,
        response: str,
        session: AsyncSession
) -> None:
    new_request = ChatRequest(
        ip_address=ip_address,
        prompt=prompt,
        response=response,
    )
    session.add(new_request)
    await session.commit()