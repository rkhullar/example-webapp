from fastapi import Depends

from ...core.router import APIRouter
from ..depends import get_identity_token, get_user
from ..schema.user import IdentityToken, User

router = APIRouter()


@router.get('/identity-token', response_model=IdentityToken)
async def read_token(identity_token: IdentityToken = Depends(get_identity_token)):
    return identity_token


@router.get('/user', response_model=User)
async def read_user(user: User = Depends(get_user)):
    return user
