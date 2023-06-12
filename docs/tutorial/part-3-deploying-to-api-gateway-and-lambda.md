# FastAPI on AWS with MongoDB Atlas and Okta - Part 3
## Deploying to API Gateway and Lambda

### TBD


In order to actually run the FastAPI code within the lambda function, we'll leverage a python library called [mangum][mangum].
This library provides an adapter to run FastAPI or other [ASGI][asgi] frameworks like [Quart][quart] or [Django][django] within
AWS Lambda. And besides API Gateway it supports integrations like Application Load Balancer (ALB) and CloudFront Lambda@Edge.

[mangum]: https://pypi.org/project/mangum
[asgi]: https://asgi.readthedocs.io/en/latest
[django]: https://www.djangoproject.com/start/overview
[quart]: https://github.com/pallets/quart
[flask]: https://flask.palletsprojects.com
