import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from starlette.requests import Request

from app.settings import settings


def get_postgresql_dsn(protocol: str = 'postgresql') -> str:
	return (
		f'{protocol}://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}'
		f'@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DATABASE}'
	)


SQLALCHEMY_DATABASE_URL = get_postgresql_dsn()

async_engine = create_async_engine(
	get_postgresql_dsn(protocol='postgresql+asyncpg'),
	future=True,
	pool_pre_ping=True,
	pool_use_lifo=True,
	# echo=True,
)
pgsql_sessionmaker = async_sessionmaker(
	bind=async_engine,
	expire_on_commit=False,
)


async def get_pgsql_session(_: Request) -> AsyncGenerator[AsyncSession, None]:
	session: AsyncSession = pgsql_sessionmaker()
	try:
		yield session
	finally:
		asyncio.shield(session.close())
