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
From the API Gateway console, build a new HTTP api called `example-backend-dev`. Add the integration to your lambda function.
Add the routes listed below which all point to the same integration. You could also add proxy routes for `PUT` and `DELETE`.
If you're looking to expand the project, those verbs are commonly used for resource updates and deletes. After the routes,
leave the default stage settings, which are `$stage` for the stage name and auto-deploy enabled.
- GET /{proxy+}
- POST /{proxy+}
- GET /docs
- GET /docs/oauth2-redirect
- GET /openapi.json

After creating the api, you should confirm that things are working so far by visiting the openapi page under the autogenerated
AWS url: `https://0123456789.execute-api.us-east-1.amazonaws.com/docs`.

At this point, if you try to log in through the openapi page, okta would come back with a 400 bad request error. You should
update your client app in okta needs to allow login the api gateway endpoint. The url path would end with `/docs/oauth2-redirect`.
If you are planning on mapping api gateway to your custom domain, then you could skip this step. But you'd only be able to
fully test the endpoints after you map the domain.

Next we should create the JWT authorizer and enable it for the proxy routes. We're trying to protect the lambda function
by having api gateway invoke it only when the caller has an active JWT from your okta developer org. Under the authorization
section for your HTTP api, create a JWT authorizer. For the name I suggest you just use your okta host name, and for the
issuer url use `https://{okta_host}/oauth2/default`. Then for the audience enter `api://default`. Attach the authorizer
to each of the proxy routes. Finally double check that you can test the endpoints from the docs page.

### Route53
If you have a custom domain registered in AWS, it's fairly easy to point a subdomain to api gateway. Let's say your domain
is `company.org` and you want your endpoints to be under `https://api-dev.example.company.org`. First you should head over
to AWS Certificate Manager (ACM) and check if you already have a certificate that can be used. If there aren't any, you
could request a certificate for `example.company.org` and `*.example.company.org`. Then AWS recommends validating domain
ownership through DNS. Follow the prompts to create the challenge records in route 53, and then wait for the certificate
to be available.

With the certificate taken care of, head back to the API Gateway console and create a custom domain name from there.
Enter `api-dev.example.company.org` for the domain name, and choose the matching certificate. Leave the endpoint type as
regional. After you've created the custom domain resource, you should map it to the api gateway stage. From the api list
select `example-backend-dev`, and for the stage select `$default`. Leave the path empty. This mapping prepares all request
to the custom domain to be handled to your HTTP api gateway by default. 

Under the endpoint configuration for the custom domain resource, take note of the generated domain name. It looks similar
to `d-0123456789.execute-api.us-east-1.amazonaws.com` Also, since you're using a custom domain, there's no need for the
first generated domain name. You can disable that endpoint under the general config for the HTTP api.

Finally head over to Route53 and review the DNS records for your domain's hosted zone, which is most likely `company.org`.
Create the new record with `api-dev.example` as the subdomain and the record type as `A`. We want the record to be an alias
record. This allows us to dynamically route traffic to API Gateway's ip addresses through the `d-` endpoint that was generated
for us. For the traffic routing options choose API Gateway and the region you've been working with. Choose the endpoint
that shows up in the dropdown and verify it matches the generated url.

Now you should be able to test the endpoints under `https://api-dev.example.company.org/docs`. The login flow should take
users to okta and back to the openapi page. And the endpoints should be storing users' posts in MongoDB Atlas.

---
Congratulations on making it the end of this tutorial. Check the [overview][overview] for additions to the series.

[mangum]: https://pypi.org/project/mangum
[asgi]: https://asgi.readthedocs.io/en/latest
[django]: https://www.djangoproject.com/start/overview
[quart]: https://github.com/pallets/quart
[flask]: https://flask.palletsprojects.com
[pandas]: https://pypi.org/project/pandas
[scikit-learn]: https://scikit-learn.org
