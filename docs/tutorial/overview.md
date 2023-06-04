# FastAPI on AWS with MongoDB Atlas and Okta

## Objective
After going through this tutorial series you'll have a better understanding of how to create backend python endpoints that
read and write to [MongoDB Atlas](https://www.mongodb.com/atlas) and are secured behind [Okta](https://developer.okta.com).

## Background
[FastAPI](https://fastapi.tiangolo.com) is a modern high performance web framework for building backend API endpoints with
python. The usage of type hints and [pydantic](https://docs.pydantic.dev/latest) for request validation makes the code
much cleaner than writing custom validation logic. And it allows the framework to generate OpenAPI docs, which makes the
endpoints easy for engineers to manually test and integrate against.

With AWS, we can deploy FastAPI or similar frameworks like Flask and Django with serverless architectures. For this
tutorial we'll use HTTP API Gateway and Lambda.

## Codebase
You can browse the code used throughout this tutorial more in depth on GitHub:
https://github.com/rkhullar/example-webapp

## Tutorial
- [Part 1: Platforms and Resource Preparation][part-1]
- [Part 2: Project Setup and Local Development][part-2]
- [Part 3: Deployment][part-3]

## Additions
- [Network Optimization][extra-1]
- [Okta vs AWS Cognito][extra-2]

[overview]: https://medium.com/@rkhullar03/fastapi-on-aws-with-mongodb-atlas-and-okta-6e37c1d9069
[part-1]: https://medium.com/@rkhullar03/fastapi-on-aws-with-mongodb-atlas-and-okta-part-1-49179c987c9
[part-2]: ""
[part-3]: ""
[extra-1]: ""
[extra-2]: ""
