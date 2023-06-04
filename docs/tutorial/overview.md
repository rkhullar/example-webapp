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

## Series
- [Part 1: Platforms and  Resource Preparation]()
- [Part 2: Project Setup]()
- [Part 3: Deployment]()
- [Network Optimization]()

