# FastAPI on AWS with MongoDB Atlas and Okta

## Objective
After reading this article you'll have an understanding of how to create backend python endpoints that read and write to
MongoDB and are secured behind okta.

## Background
[FastAPI](https://fastapi.tiangolo.com) is a modern high performance web framework for building backend API endpoints with
python. The usage of type hints and [pydantic](https://docs.pydantic.dev/latest) for request validation makes the code
much cleaner than writing custom validation logic. And it allows the framework to generate OpenAPI docs, which makes the
endpoints easy for engineers to manually test and integrate against.

With AWS, we can deploy FastAPI or similar frameworks like Flask and Django with a serverless architecture. For this
article we'll use HTTP API Gateway and Lambda.

### Codebase
The code used throughout this article is available at the following url:
https://github.com/rkhullar/example-webapp

## Platforms
### Amazon Web Services (AWS)
You will need access to an AWS account to follow along and deploy the example api. If you are deploying to your own account
remember to clean up the resources afterward to keeping billing charges to a minimum. I would also suggest setting up
billing alerts and using a service like [privacy.com](https://privacy.com) to prevent overcharging. If you do not have an
AWS account you could try using the lab environment on [A Cloud Guru](https://learn.acloud.guru/labs).

### MongoDB Atlas
If you haven't already, head over to [MongoDB Cloud](https://www.mongodb.com/cloud) to create a free tier Atlas cluster.
Within your organization namespace create a `dev` project. And within that project create a shared cluster called
`default-free-dev` backed by AWS and located in the closest available region to you. For example if you are based in
New York the region would be `us-east-1`. There are more details for creating the cluster in the tutorial section below.

### Okta
You can sign up for a free okta developer account by heading to their [developer login page](https://developer.okta.com/login).
After signing up you could optionally customize your org by setting a custom domain name and adding social login. That is
not the focus of this article, but the following links should help:
- https://developer.okta.com/docs/guides/custom-url-domain/main/#use-an-okta-managed-certificate
- https://developer.okta.com/docs/guides/social-login/google/main/

## Tutorial

### Resource Preparation
#### AWS User and Lambda Role
For this tutorial we are managing database access to the data layer through AWS IAM. During local development you should
have your `AWS_PROFILE` configured, which points to the credentials uses for AWS integrations: `aws_access_key_id`
`aws_secret_access_key` and for roles `aws_session_token`. When you create the IAM user in your AWS account be sure to
follow good security practices like adding MFA and using a strong password.

When we create the lambda function later on we will need to specify the role. So let's create the role with the name
`example-backend-dev` and the `AWSLambdaBasicExecutionRole` managed policy. The trust relationship for the role should
define `lambda.amazonaws.com` as the service, which means that the role can be assumed by any lambda function in the account.

#### Mongodb Atlas Cluster
During the cluster creation process the Atlas UI will ask you to create database user credentials and define the ip address
or cidr blocks that should be allowed to connect. You can go ahead and use the default generated credentials. We don't
actually need database credentials for our project, and will instead leverage passwordless authentication via AWS Identity
Access Management (IAM). For the ip address list we need to allow network traffic from `0.0.0.0/0` "anywhere". For a production
environment we can revisit this network control, but there is significantly more work involved to make the ideal integration.
And it does not fall under AWS or Atlas free tier.

After creating the cluster delete the default credential based user and replace it with your AWS user arn. When you
add the new database user in the Atlas UI select AWS IAM for the authentication method and select IAM User for the type.
For the database user privileges choose the built-in role "read and write to any database". And as a good practice you
should explicitly define which cluster the permissions apply to.

This would also be a good time to create another database user that represents the lambda function we're deploying to later on.
This type select IAM Role to the type and enter the lambda role arn. And for the permissions we want to follow the principle
of least privilege. So for this example project we'll define a single permission: `readWrite` to the `default` database
`message` collection.

We wll need the cluster host value during local development and the deployment. On the Atlas UI you can find out the value
from following the instruction to connect to the cluster. We don't need the full connection url, just the host value. It
should look similar to this: `default-free-dev.example.mongodb.net`

#### Okta 

### Project Setup
#### Virtual Environment
At the time of this writing the aws lambda runtime runs with python `3.10.9`. You can use a program like [`asdf`](https://asdf-vm.com)
to manage multiple versions of developer tools. In your project workspace use the following commands to create a virtual
environment and install the required libraries. As you add dependencies with `pipenv` they will be tracked with a `Pipfile`.

```shell
python -m venv venv
. venv/bin/activate
pip install -U pip setuptools
pip install pipenv
pipenv install fastapi mangum 'pymongo[aws,srv]'
pipenv install --dev uvicorn
```

#### File Tree
Within the project workspace we will create the following structure:
```text
|-- api
|   |-- __init__.py
|   |-- config.py
|   |-- depends.py
|   |-- factory.py
|   |-- model
|   |   |-- __init__.py
|   |   |-- document.py
|   |   |-- message.py
|   |   `-- object_id.py
|   |-- router.py
|   |-- routes
|   |   |-- __init__.py
|   |   `-- message.py
|   `-- schema
|       |-- __init__.py
|       |-- message.py
|       `-- user.py
|-- lambda_function.py
`-- server.py
```

This structure encapsulate almost of all the fastapi logic into the `api` package. The `server` module should be used
for local development or containerized deployments, and the `lambda_function` module will be used in our AWS lambda deployment.
The idea behind `model` `routes` and `schema` being packages is to keep the project well organized as it expands with new features.
Each top level data resource would be defined under `model`, the routes to manage that data model would be under `routes`,
and the request and response schema for those routes would be under `schema`.

### Local Development

To start local development we will focus on the following four modules: `config` `router` `factory` `server`.
```python
# api/config.py

from pydantic import BaseSettings
import os

class ProjectSettings(BaseSettings):
    environment: str = os.environ['ENVIRONMENT']
    debug: bool = bool(os.getenv('DEBUG'))

class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))

class OktaSettings(BaseSettings):
    okta_host: str = os.environ['OKTA_HOST']
    okta_client_id: str = os.environ['OKTA_CLIENT_ID']

class MongoSettings(BaseSettings):
    atlas_host: str = os.environ['ATLAS_HOST']

class Settings(ProjectSettings, NetworkSettings, OktaSettings, MongoSettings):
    pass
```

```python
# api/router.py

from fastapi import APIRouter

router = APIRouter()

@router.get('/hello-world')
async def hello_world():
    return dict(message='hello world')
```

```python
# api/factory.py

from fastapi import FastAPI
from pymongo import MongoClient
from .config import Settings
from .router import router as api_router

def build_atlas_client(atlas_host: str) -> MongoClient:
    mongo_client_url = f'mongodb+srv://{atlas_host}/?authSource=%24external&authMechanism=MONGODB-AWS&retryWrites=true&w=majority'
    return MongoClient(mongo_client_url, connect=True)

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        settings=settings,
        swagger_ui_init_oauth={
            'clientId': settings.okta_client_id,
            'usePkceWithAuthorizationCodeGrant': True,
            'scopes': ' '.join(['openid', 'profile', 'email'])
        }
    )
    app.include_router(api_router)
    app.extra['mongo_client'] = build_atlas_client(atlas_host=settings.atlas_host)
    return app
```

```python
# server.py

from api.config import Settings
from api.factory import create_app
from fastapi import FastAPI

settings: Settings = Settings()
app: FastAPI = create_app(settings)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('server:app', host=settings.service_host, port=settings.service_port, reload=settings.debug)
```

