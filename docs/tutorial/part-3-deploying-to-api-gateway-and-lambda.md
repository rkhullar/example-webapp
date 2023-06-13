# FastAPI on AWS with MongoDB Atlas and Okta - Part 3
## Deploying to API Gateway and Lambda

### Lambda Layer
- Dockerfile
- build.sh
- Pipfile
- docker-compose.yaml

Run `docker-compose up` to build the lambda layer package within docker and copy the zip file onto your host machine.

### ASGI in Lambda: Mangum
In order to actually run the FastAPI code within the lambda function, we'll leverage a python library called [mangum][mangum].
This library provides an adapter to run FastAPI or other [ASGI][asgi] frameworks like [Quart][quart] or [Django][django] within
AWS Lambda. And besides API Gateway it supports integrations like Application Load Balancer (ALB) and CloudFront Lambda@Edge.

### Lambda Function
From the Lambda console, create a new function called `example-backend-test`. Select the current python version for the
runtime, and `arm64` for the Architecture. Under permissions change the execution role to `example-backend-dev`, which we
created in [Part 1][part-1].

In the function overview, attach the custom `example-backend` layer to the function runtime. Under the function configuration
add the required environment variables which were used during local development. Under the general configuration review
the memory and timeout and optionally increase them. The default timeout is 3 seconds, but the max is 29 seconds for integrating
with API Gateway.

Finally, run the `build.sh` script for the function package and upload it to the lambda source code.

### API Gateway
- From the API Gateway console, build a new HTTP api called `example-backend-dev`

## Continue
- [Overview][overview]

[mangum]: https://pypi.org/project/mangum
[asgi]: https://asgi.readthedocs.io/en/latest
[django]: https://www.djangoproject.com/start/overview
[quart]: https://github.com/pallets/quart
[flask]: https://flask.palletsprojects.com
