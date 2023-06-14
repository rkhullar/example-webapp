# FastAPI on AWS with MongoDB Atlas and Okta - Part 3
## Deploying to API Gateway and Lambda

Now that we have the endpoints and their integrations tested locally, it's time to deploy them into AWS. As I mentioned
in the [overview][overview] we're going to use API Gateway (HTTP) and Lambda for the architecture. It's relatively
quick to set up, it's low cost for our traffic volume, and it comes with JWT authorization.

We'll deploy the components according to dependency. First we'll create the lambda layer which provides the python libraries
that are needed at runtime. We'll work on the entrypoint for the lambda functon. Then we'll create the lambda function,
build the `package.zip` from the source code, and deploy it to the lambda function. Lastly we'll go through the HTTP API
setup and optionally map it to a custom domain with Route53. Don't forget to clean up your deployment resources afterwards.

### Lambda Layer
Using a lambda layer allows us to nicely decouple source code from its library dependencies. As your project expands you'll
update your lambda function code much more often then the library versions. Decoupling also makes your CI builds faster and
reduces storage costs. If you're running many builds without updating to the `Pipfile`, then the pipeline doesn't need to
run `pip install` for each one. The time saved adds up with more features being worked on and more team members joining
the project. Making builds faster and the deployment more stable are significant boosts to developer productivity.

The key input to building the lambda layer archive is the `Pipfile`. You should already have one in your project from
the virtual environment setup in [part 2][part-2]. We're using docker when we build the layer archive since it'll provide
some consistency between your local machine and AWS. That's especially useful if you want to use the `arm64` for the lambda
function, but don't have that on your machine. Or if you're using a python library with compiled extensions, like
[`pandas`][pandas] or [`scikit-learn`][scikit-learn].

Create a new folder in your project called `layer-docker` and copy the following files into it.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-pipfile.toml
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer.dockerfile
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-build.sh
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-docker-compose.yaml

Run `chmod +x build.sh` so that the Dockerfile can execute the helper script. And then run `docker-compose up`. This should
build the lambda layer archive within docker and copy the result onto your host machine.

From the AWS Lambda console, create a new layer called `example-backend`. Select the current supported python version for
the compatible runtimes, and select `arm64` for the compatible architectures. Upload the `zip` file we got from the previous
step.

### Lambda Function - Entrypoint
In order to actually run the FastAPI code within the lambda function, we'll leverage a python library called [mangum][mangum].
This library provides an adapter to run FastAPI or other [ASGI][asgi] frameworks like [Quart][quart] or [Django][django] within
AWS Lambda. And besides API Gateway it supports integrations like Application Load Balancer (ALB) and CloudFront Lambda@Edge.

The following code is all we need for the lambda function entrypoint. It's also possible to add custom logic at the request,
but that's for more advanced scenarios.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=lambda-function.yaml

### Lambda Function
From the Lambda console, create a new function called `example-backend-dev`. Select the current python version for the
runtime, and `arm64` for the architecture. Under permissions, change the execution role to `example-backend-dev`. That role
should already be created from [part 1][part-1].

In the function overview, attach the custom `example-backend` layer to the function runtime. Under the function configuration,
add the required environment variables which were used during local development. Under the general configuration, review
the memory and timeout and optionally increase those value. The default timeout is 3 seconds, but the max is 29 seconds
for integrating with API Gateway.

Now we need to create the function package and upload it to the lambda source code. Copy the following script into your
project. When you run `./build.sh` it should create the `package.zip` file under a new folder, `local/dist`. The script
uses the `find` shell command to clean up things like pycache and unit tests, which aren't needed during runtime.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=function-build.sh

### API Gateway
- From the API Gateway console, build a new HTTP api called `example-backend-dev`

---
Congratulations on making it the end of this tutorial. Check the [overview][overview] for additions to the series.

[mangum]: https://pypi.org/project/mangum
[asgi]: https://asgi.readthedocs.io/en/latest
[django]: https://www.djangoproject.com/start/overview
[quart]: https://github.com/pallets/quart
[flask]: https://flask.palletsprojects.com
[pandas]: https://pypi.org/project/pandas
[scikit-learn]: https://scikit-learn.org
