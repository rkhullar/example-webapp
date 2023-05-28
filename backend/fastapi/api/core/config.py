import os

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.getenv('PROJECT', 'hello-world')
    environment: str = os.environ['ENVIRONMENT']
    reload_fastapi: bool = 'RELOAD_FASTAPI' in os.environ


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class OktaSettings(BaseSettings):
    okta_host: str = os.environ['OKTA_HOST']
    okta_client_id: str = os.environ['OKTA_CLIENT_ID']


class MongoSettings(BaseSettings):
    atlas_host: str = os.environ['ATLAS_HOST']
    local_mode: bool = 'LOCAL_MODE' in os.environ


class Settings(ProjectSettings, NetworkSettings, OktaSettings, MongoSettings):
    pass
