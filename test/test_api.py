import uuid

import pytest
from aiohttp import ClientSession

from src.constants import AUTH_URL, CREATE_PET_URL


@pytest.mark.asyncio
async def test_auth(session: ClientSession, auth_data: dict[str, str]):
    response = await session.get(AUTH_URL, headers=auth_data)
    assert response.status == 200

    response_body = await response.json()
    assert response_body["key"]


@pytest.mark.asyncio
async def test_auth_error(session: ClientSession):
    auth_data = {
        "email": "asd@asd.com",
        "password": "1234567"
    }

    response = await session.get(AUTH_URL, headers=auth_data)

    assert response.status == 403


@pytest.mark.asyncio
async def test_auth_without_password(session: ClientSession):
    auth_data = {
        "email": "asd@asd.com",
    }

    response = await session.get(AUTH_URL, headers=auth_data)

    assert response.status == 403


@pytest.mark.asyncio
async def test_auth_without_email(session: ClientSession):
    auth_data = {
        "password": "1234567"
    }

    response = await session.get(AUTH_URL, headers=auth_data)

    assert response.status == 403


@pytest.mark.asyncio
async def test_auth_without_headers(session: ClientSession):
    response = await session.get(AUTH_URL)

    assert response.status == 403


@pytest.mark.asyncio
async def test_create_pet(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert pet_data["name"] == body["name"]


@pytest.mark.asyncio
async def test_create_pet_wo_name(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data.pop("name")

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 500


@pytest.mark.asyncio
async def test_create_pet_wo_age(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data.pop("age")

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 500


@pytest.mark.asyncio
async def test_create_pet_wo_animal_type(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data.pop("animal_type")

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 500


@pytest.mark.asyncio
async def test_create_pet_wo_pet_data(session: ClientSession, auth_key: dict[str, str]):
    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key
    )
    assert response.status == 400


@pytest.mark.asyncio
async def test_create_pet_wo_auth_key(session: ClientSession, pet_data: dict):
    response = await session.post(
        CREATE_PET_URL,
        json=pet_data,
    )
    assert response.status == 403


@pytest.mark.asyncio
async def test_create_pet_with_incorrect_animal_type(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["animal_type"] = "dfhajksdl;fkasdj;flsajfioqwueqoito[p]qt"

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert pet_data["animal_type"] == body["animal_type"]


@pytest.mark.asyncio
async def test_create_pet_with_too_long_name(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["name"] = "lorem ipsum" * 300

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert pet_data["name"] == body["name"]


@pytest.mark.asyncio
async def test_create_pet_with_big_age(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["age"] = 1_000_000_000

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert str(pet_data["age"]) == body["age"]


@pytest.mark.asyncio
async def test_create_pet_with_str_age(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["age"] = "1000000000"

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert pet_data["age"] == body["age"]


@pytest.mark.asyncio
async def test_create_pet_with_text_age(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["age"] = "text_age"

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert pet_data["age"] == body["age"]


@pytest.mark.asyncio
async def test_create_pet_with_number_animal_type(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["animal_type"] = 120

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert str(pet_data["age"]) == body["age"]


@pytest.mark.asyncio
async def test_create_pet_with_number_name(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["name"] = 199

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert str(pet_data["name"]) == body["name"]


@pytest.mark.asyncio
async def test_create_pet_with_number_name(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["name"] = 199

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200

    body = await response.json()
    assert str(pet_data["name"]) == body["name"]


@pytest.mark.asyncio
async def test_create_pet_with_additional_params(session: ClientSession, auth_key: dict[str, str], pet_data: dict):
    pet_data["asdqweqr"] = '12s'

    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 200


@pytest.mark.asyncio
async def test_create_pet_with_uuid_on_auth_key(session: ClientSession, pet_data: dict):
    auth_key = {
        "auth_key": str(uuid.uuid4()),
    }
    response = await session.post(
        CREATE_PET_URL,
        headers=auth_key,
        json=pet_data,
    )
    assert response.status == 403
