import os

from pydantic import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.getenv('PROJECT', 'hello-world')
    environment: str = os.getenv('ENVIRONMENT')
    debug: bool = bool(os.getenv('DEBUG'))


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class OktaSettings(BaseSettings):
    okta_host: str = os.getenv('OKTA_HOST')
    okta_client_id: str = os.getenv('OKTA_CLIENT_ID')


class MongoSettings(BaseSettings):
    atlas_host: str = os.getenv('ATLAS_HOST')


class Settings(ProjectSettings, NetworkSettings, OktaSettings, MongoSettings):
    pass
