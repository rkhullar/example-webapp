from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from .graphql import schema
from .routes import debug, message

router = APIRouter()
router.include_router(debug.router, prefix='/debug', tags=['debug'])
router.include_router(message.router, prefix='/message', tags=['example'])
router.include_router(GraphQLRouter(schema), prefix='/graphql', tags=['graphql'], include_in_schema=False)
