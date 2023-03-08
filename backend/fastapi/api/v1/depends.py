import os

from fastapi import Depends

from ..core.util import BearerAuth, OktaAuthCodeBearer, async_httpx
from .schema.user import IdentityToken, User

okta_host = os.getenv('OKTA_HOST')
auth_scheme = OktaAuthCodeBearer(domain=okta_host)


async def get_identity_token(access_token: str = Depends(auth_scheme)) -> IdentityToken:
    response = await async_httpx(method='get', url=auth_scheme.userinfo_url, auth=BearerAuth(access_token))
    response.raise_for_status()
    return IdentityToken(**response.json())


async def get_user(identity_token: IdentityToken = Depends(get_identity_token)) -> User:
    # TODO: distinguish between active and inactive?
    return User.from_token(token=identity_token)
