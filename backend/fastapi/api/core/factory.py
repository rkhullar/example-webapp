from fastapi import FastAPI

from ..model.adapter import MongoAdapterCache
from ..router import router as api_router
from .config import Settings
from .util import build_atlas_client


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
    mongo_client = build_atlas_client(atlas_host=settings.atlas_host, local_mode=settings.reload_fastapi)
    app.extra['atlas'] = MongoAdapterCache(mongo_client=mongo_client)
    return app
