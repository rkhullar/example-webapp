from fastapi import Depends

from ...core.router import APIRouter
from ..depends import GetUser, get_identity_token
from ..schema.user import OktaIdentityToken, User

router = APIRouter()


@router.get('/identity-token', response_model=OktaIdentityToken)
async def read_token(identity_token: OktaIdentityToken = Depends(get_identity_token)):
    return identity_token


@router.get('/user', response_model=User)
async def read_user(user: GetUser):
    return user
