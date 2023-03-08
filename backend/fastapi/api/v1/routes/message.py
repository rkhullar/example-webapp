import os

from fastapi import Depends, HTTPException, status

from ...core.router import APIRouter
from ...core.util import build_atlas_client
from ...model.message import Message
from ..depends import get_user
from ..schema.message import CreateMessage
from ..schema.user import User

router = APIRouter()
atlas_host: str = os.getenv('ATLAS_HOST')
local_mode: bool = 'LOCAL_MODE' in os.environ
mongo_client = build_atlas_client(atlas_host, local_mode)
collection = mongo_client.get_database('default').get_collection('message')


@router.get('', response_model=list[Message])
async def list_messages(user: User = Depends(get_user)):
    # TODO: generic crud response types and pagination
    if 'internal/example/admins' not in user.groups:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return [Message.from_pymongo(doc) for doc in collection.find()]


@router.post('', response_model=Message)
async def create_message(create_object: CreateMessage, user: User = Depends(get_user)):
    to_insert = create_object.to_pymongo(okta_id=user.okta_id)
    response = collection.insert_one(to_insert)
    return Message(
        id=response.inserted_id,
        created=to_insert['created'],
        okta_id=to_insert['okta_id'],
        message=create_object.message
    )
