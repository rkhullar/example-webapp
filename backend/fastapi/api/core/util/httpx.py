from dataclasses import dataclass

import httpx


async def async_httpx(method: str, *args, **kwargs):
    async with httpx.AsyncClient() as client:
        fn = getattr(client, method)
        return await fn(*args, **kwargs)


@dataclass
class BearerAuth(httpx.Auth):
    token: str

    def auth_flow(self, request):
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request
