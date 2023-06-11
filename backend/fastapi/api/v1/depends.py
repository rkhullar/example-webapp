import os
from typing import Annotated, Type

from pymongo.collection import Collection

from fastapi import Depends, Query, Request

from ..core.util import BearerAuth, OktaAuthCodeBearer, async_httpx
from ..model.adapter import MongoAdapter, MongoAdapterCache
from ..model.document import DocumentType
from .schema.user import OktaIdentityToken, OktaUser, User

okta_host = os.getenv('OKTA_HOST')
auth_scheme = OktaAuthCodeBearer(domain=okta_host)


async def get_identity_token(access_token: str = Depends(auth_scheme)) -> OktaIdentityToken:
    response = await async_httpx(method='get', url=auth_scheme.userinfo_url, auth=BearerAuth(access_token))
    response.raise_for_status()
    return OktaIdentityToken(**response.json())


async def get_user(identity_token: OktaIdentityToken = Depends(get_identity_token)) -> OktaUser:
    # TODO: distinguish between active and inactive?
    return OktaUser.from_token(token=identity_token)


GetUser = Annotated[User, Depends(get_user)]


def atlas(name: str, database: str = 'default', model: Type[DocumentType] = None):
    # TODO: rename and split into helpers for loading adapter and collection
    def dependency(request: Request) -> MongoAdapter[DocumentType] | Collection:
        mongo_adapter_cache: MongoAdapterCache = request.app.extra['atlas']
        if model:
            return mongo_adapter_cache.adapter(collection=name, database=database, model_type=model)
        else:
            return mongo_adapter_cache.collection(collection=name, database=database)
    return_type = MongoAdapter[DocumentType] if model else Collection
    return Annotated[return_type, Depends(dependency)]


def annotated_query(_type, **kwargs):
    return Annotated[_type, Query(**kwargs)]


def int_query(**kwargs):
    return annotated_query(int, **kwargs)
