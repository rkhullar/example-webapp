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
New York the region would be `us-east-1`.

### Okta
You can sign up for a free okta developer account by heading to their [developer login page](https://developer.okta.com/login).
After signing up you could optionally customize your org by setting a custom domain name and adding social login. That is
not the focus of this article, but the following links should help:
- https://developer.okta.com/docs/guides/custom-url-domain/main/#use-an-okta-managed-certificate
- https://developer.okta.com/docs/guides/social-login/google/main/

## Tutorial
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
Within the project workspace we will need the following structure:
```text
|-- api
|   |-- __init__.py
|   |-- config.py
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
