from fastapi import FastAPI

from ..router import router as api_router
from .config import Settings


def create_app(settings: Settings, test: bool = False) -> FastAPI:
    app = FastAPI(
        settings=settings,
        swagger_ui_init_oauth={
            'clientId': settings.okta_client_id,
            'usePkceWithAuthorizationCodeGrant': True,
            'scopes': ' '.join(['openid', 'profile', 'email'])
        }
    )
    app.include_router(api_router)  # prefix='/api'
    return app
