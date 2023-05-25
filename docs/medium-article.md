# FastAPI on AWS with MongoDB Atlas and Okta

## Objective
After reading this article you'll have an understanding of how to create backend python endpoints that read and write to
MongoDB and are secured with openid connect (OIDC). 

## Background
[FastAPI](https://fastapi.tiangolo.com) is currently my preferred web framework for building backend API endpoints with
python. The usage of type hints and [pydantic](https://docs.pydantic.dev/latest) for request validation makes the code
much cleaner than writing custom validation logic. And it allows the framework to generate OpenAPI docs, which makes the
endpoints much easier to integrate with and test.

With AWS, we can deploy FastAPI or similar frameworks like Flask and Django with a serverless architecture. For this
article we'll use HTTP API Gateway and Lambda.

## Codebase
https://github.com/rkhullar/example-webapp

## Platforms
### Amazon Web Services (AWS)
You will need access to an AWS account to follow along and deploy the example api. If you are deploying to your own account
remember to clean up the resources afterward to keeping billing charges to a minimum. I would also suggest setting up
billing alerts and using a service like [privacy.com](https://privacy.com) to prevent overcharging. If you do not have an
account you could try using the lab environment on [A Cloud Guru](https://learn.acloud.guru/labs).

### MongoDB Atlas
If you haven't already, head over to [MongoDB Cloud](https://www.mongodb.com/cloud) to create a free tier Atlas cluster.
Within your organization namespace create a `dev` project. And within that project create a shared cluster called
`default-free-dev` backed by AWS and located in the closest available region to you. For example if you are based in
New York that region would be `us-east-1`.

### Okta
You can sign up for a free okta developer account by heading to their [developer login page](https://developer.okta.com/login).
After signing up you could optionally customize your org by setting a custom domain name and adding social login. That is
not the focus of this article, but the following links should help:
- https://developer.okta.com/docs/guides/custom-url-domain/main/#use-an-okta-managed-certificate
- https://developer.okta.com/docs/guides/social-login/google/main/

