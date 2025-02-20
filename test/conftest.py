from typing import AsyncIterable

import pytest
import pytest_asyncio
from aiohttp import ClientSession

from src.constants import AUTH_URL
from src.main import config


@pytest_asyncio.fixture
async def session() -> AsyncIterable[ClientSession]:
    async with ClientSession() as client_session:
        yield client_session


@pytest.fixture
def auth_data() -> dict[str, str]:
    return config.auth.auth_data


@pytest_asyncio.fixture
async def auth_key(session: ClientSession, auth_data: dict[str, str]) -> dict[str, str]:
    response = await session.get(AUTH_URL, headers=auth_data)
    response_body = await response.json()
    return {"auth_key": response_body["key"], }


@pytest.fixture
def pet_data() -> dict[str, str | int]:
    return {
        "name": "Barbos",
        "animal_type": "German Shepherd",
        "age": 2
    }
