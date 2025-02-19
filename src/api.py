from aiohttp import ClientSession


class HTTPClient:
    _API_URL = "https://petfriends.skillfactory.ru/api"
    _AUTH_URL = f"{_API_URL}/key"
    _CREATE_PET_URL = f"{_API_URL}/create_pet_simple"
    _GET_PETS_URL = f"{_API_URL}/pets"
    _DELETE_PET_URL = f"{_API_URL}/pets"
    _UPDATE_PET_URL = f"{_API_URL}/pets"

    def __init__(self, session: ClientSession):
        self._session = session

    async def auth(self, auth_data: dict[str, str]) -> None:
        key = await self._session.get(self._AUTH_URL, headers=auth_data)
