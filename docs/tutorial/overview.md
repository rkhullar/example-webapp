# FastAPI on AWS with MongoDB Atlas and Okta

## Objective
After going through this tutorial series you'll have a better understanding of how to create backend python endpoints that
read and write to [MongoDB Atlas][mongodb-atlas] and are secured behind [Okta][okta].

## Background
[FastAPI][fastapi] is a modern high-performance web framework for building backend API endpoints with Python. The usage of
type hints and [pydantic][pydantic] for request validation makes the code much cleaner than writing custom validation logic.
And it allows the framework to generate OpenAPI docs, which makes the endpoints easy for engineers to manually test and
integrate against.

## Architecture
![](images/architecture-sequence-diagram.png)

We'll be deploying the backend endpoints to AWS API Gateway and Lambda, which gives us a common type of serverless architecture
that's relatively easy to get started with and should have little to no cost at 20 api requests per minute. There are two
main types of endpoints under API Gateway, REST and HTTP. We'll be using HTTP since it features built in support for JWT
authorization. That's key to protect the lambda function from being invoked by bots or bad actors. [Part 3][part-3] of the
tutorial walks through the deployment details after you're able to develop and test out the endpoints locally.

## Codebase
You can browse the code used throughout this tutorial more in depth on GitHub:
https://github.com/rkhullar/example-webapp

## Tutorial
- [Part 1: Platforms and Resource Preparation][part-1]
- [Part 2: Project Setup and Local Development][part-2]
- [Part 3: Deploying to API Gateway and Lambda][part-3]

[fastapi]: https://fastapi.tiangolo.com
[mongodb-atlas]: https://www.mongodb.com/atlas
[okta]: https://developer.okta.com
[pydantic]: https://docs.pydantic.dev/latest
