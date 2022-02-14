from typing import Any, Literal, Optional

from aiohttp import ClientSession


class BaseHTTP:
    def __init__(self, session: Optional[ClientSession] = None) -> None:
        self.session = session

    async def request(
        self,
        method: Literal["GET", "POST", "DELETE", "PUT", "PATCH"],
        url: str,
        **kwargs: Any,
    ) -> Any:
        if not self.session:
            self.session = ClientSession()
        async with self.session.request(method, url, **kwargs) as r:
            if r.status == 204:
                return {}
            r.raise_for_status()
            return await r.json()

    async def get(self, path: str, **kwargs: Any) -> Any:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs: Any) -> Any:
        return await self.request("POST", path, **kwargs)

    async def delete(self, path: str, **kwargs: Any) -> Any:
        return await self.request("DELETE", path, **kwargs)

    async def put(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PUT", path, **kwargs)

    async def patch(self, path: str, **kwargs: Any) -> Any:
        return await self.request("PATCH", path, **kwargs)

    async def close(self) -> None:
        if self.session:
            await self.session.close()


class DiscordBaseHTTP(BaseHTTP):
    BASE_URL = "https://discord.com/api"
    VERSION = "v9"
    FULL_URL = f"{BASE_URL}/{VERSION}"

    def __init__(self, token: str, session: Optional[ClientSession] = None) -> None:
        super().__init__(session=session)
        self.token = token

    async def request(
        self,
        method: Literal["GET", "POST", "DELETE", "PUT", "PATCH"],
        url: str,
        **kwargs: Any,
    ) -> Any:
        if not self.session:
            self.session = ClientSession(headers={"Authorization": f"Bot {self.token}"})
        return await super().request(method, f"{self.FULL_URL}{url}", **kwargs)

    async def channel_is_nsfw(self, channel_id: int) -> bool:
        res = await self.get(f"/channels/{channel_id}")
        if res.get("nsfw"):
            return True
        return False
