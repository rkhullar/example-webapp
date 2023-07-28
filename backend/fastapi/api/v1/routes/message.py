from fastapi import HTTPException, status

from ...core.router import APIRouter
from ...model.message import Message
from ..depends import GetUser, atlas
from ..schema.crud import ListResponse
from ..schema.message import CreateMessage

router = APIRouter()
MessageAdapter = atlas(name='message', model=Message)


@router.get('', response_model=ListResponse[Message])
async def list_messages(user: GetUser, adapter: MessageAdapter):
    require_admin_role: bool = False
    if require_admin_role and 'internal/example/admins' not in user.groups:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return ListResponse(data=adapter.iter_docs())


@router.post('', response_model=Message)
async def create_message(user: GetUser, adapter: MessageAdapter, create_object: CreateMessage):
    to_insert = create_object.to_pymongo(user_id=user.id)
    response = adapter.collection.insert_one(to_insert)
    return Message(
        id=response.inserted_id,
        created=to_insert['created'],
        user_id=to_insert['user_id'],
        message=create_object.message
    )
