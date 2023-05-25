# FastAPI on AWS with MongoDB Atlas and Okta

FastAPI is currently my preferred web framework for building backend API endpoints with python. The usage of type hints
and pydantic for request validation makes the code much cleaner than writing custom validation logic. And it allows the
framework to generate OpenAPI docs, which makes the endpoints much easier to integrate with and test.

With AWS, we can deploy FastAPI or similar frameworks like Flask and Django with a serverless architecture. For this
article we'll use API Gateway and Lambda. But another popular archetype would be with an Application Load Balancer (ALB)
and ECS Fargate.
