from mangum import Mangum

from api.core.config import Settings
from api.core.factory import create_app
from fastapi import FastAPI

settings: Settings = Settings()
app: FastAPI = create_app(settings)
lambda_handler: Mangum = Mangum(app)
