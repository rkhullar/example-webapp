# FastAPI on AWS with MongoDB Atlas and Okta - Part 3
## Deploying to API Gateway and Lambda

Now that we have the endpoints and their integrations tested locally, it's time to deploy them into AWS. As mentioned in
the [overview][overview], we're going to use HTTP API Gateway and Lambda for the architecture. It's relatively quick to
set up, it's low cost for our traffic volume, and it comes with JWT authorization.

We'll deploy the components according to dependency. First we'll create the lambda layer which provides the python libraries
that are needed at runtime. We'll work on the entrypoint for the lambda function. Then we'll create the lambda function,
build the `package.zip` from the source code, and update the function code. Lastly we'll go through the HTTP API setup
and optionally map it to a custom domain with Route53. Don't forget to clean up your deployment resources afterwards.

### Lambda Layer
Using a lambda layer allows us to nicely decouple source code from its library dependencies. As your project expands you'll
update your lambda function code more frequently then the library versions. Decoupling also makes your CI builds faster and
reduces storage costs. If you're running many builds without updating the `Pipfile`, then the pipeline doesn't need to
run `pip install` for each one. The time saved adds up with more features being worked on and more team members joining
the project. It significantly boosts developer productivity.

The main input to building the lambda layer archive is the `Pipfile`. You should already have one in your project from
the virtual environment setup in [part 2][part-2]. We're using docker to build the layer archive since it'll provide
consistency between your local machine and AWS. That's especially useful if you want to use the `arm64` for the lambda
function, but don't have that on your machine. Or if you're using a python library with compiled extensions, like
[`pandas`][pandas] or [`scikit-learn`][scikit-learn].

Create a new folder in your project called `layer-docker` and copy the following files into it.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-pipfile.toml
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer.dockerfile
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-build.sh
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=layer-docker-compose.yaml

Run `chmod +x build.sh` so that docker can use the helper script. And then run `docker-compose up`. This should build the
lambda layer archive within docker and copy the result onto your host machine.

From the AWS Lambda console, create a new layer called `example-backend`. Select the current supported python version for
the compatible runtimes, and select `arm64` for the compatible architectures. Upload the `zip` file we got from the previous
step.

### Lambda Function - Entrypoint
In order to actually run the FastAPI code within the lambda function, we'll leverage a python library called [mangum][mangum].
This library provides an adapter to run FastAPI or other [ASGI][asgi] frameworks like [Quart][quart] or [Django][django]
within AWS Lambda. Besides API Gateway it also supports integrations like Application Load Balancer (ALB) and CloudFront
Lambda@Edge.

The following code is all we need for the lambda function entrypoint. It's possible to add custom logic at the request,
but that's for more advanced scenarios.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=lambda-function.yaml

### Lambda Function
From the lambda console, create a new function called `example-backend-dev`. Select the current python version for the
runtime, and `arm64` for the architecture. Under permissions, change the execution role to `example-backend-dev`. That role
should already be created from [part 1][part-1].

In the function overview, attach the custom `example-backend` layer to the function runtime. Under the function configuration,
add the required environment variables that you used during local development. Under the general configuration, review and
optionally increase the values for memory and timeout. The default timeout is 3 seconds, but the max for integrating with
API Gateway is 29 seconds.

Now we need to create the source package and upload it to the lambda function. Copy the below script into your project.
When you run `./build.sh` it should create the `package.zip` file under a new folder, `local/dist`. The script uses the
`find` shell command to clean up things like pycache and unit tests, which aren't needed during runtime.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=function-build.sh

### API Gateway
From the API Gateway console, build a new HTTP api called `example-backend-dev`. Add the integration to your lambda function.
And add the routes listed below which should all point to the same lambda integration. You could also add proxy routes for
`PUT` and `DELETE`. If you're looking to expand the project, those verbs are commonly used for resource updates and deletes.
After creating the routes, continue with the default stage settings, which are `$stage` for the stage name and auto-deploy
enabled.
- GET /{proxy+}
- POST /{proxy+}
- GET /docs
- GET /docs/oauth2-redirect
- GET /openapi.json

After creating the api, you should confirm that things are working so far by visiting the openapi page under the autogenerated
AWS url: `https://0123456789.execute-api.us-east-1.amazonaws.com/docs`.

At this point, if you try to log in through the openapi page, okta would come back with a 400 bad request error. You should
update your client app in okta to allow logins the api gateway endpoint. The url path would end with `/docs/oauth2-redirect`.
If you are planning on mapping api gateway to your custom domain, then you could skip this step. But you'd only be able to
fully test the endpoints after you map the domain.

Next we should create the JWT authorizer and enable it for the proxy routes. We're trying to protect the lambda function
by having api gateway invoke it only when the caller has an active JWT from your okta developer org. Under the authorization
section for your HTTP api, create a JWT authorizer. For the name I suggest you just use your okta host name, and for the
issuer url use `https://{okta_host}/oauth2/default`. Then for the audience enter `api://default`. Attach the authorizer
to each of the proxy routes. Double check that you're still able to test the endpoints from the docs page.

### Route53
If you have a custom domain registered in AWS, it's fairly easy to point a subdomain to api gateway. Let's say your domain
is `company.org` and you want your endpoints to be under `https://api-dev.example.company.org`. First you should head over
to AWS Certificate Manager (ACM) and check if you already have a certificate that can be used. If there's none available,
you could request a certificate for `example.company.org` and `*.example.company.org`. Before the certificates are issued,
AWS would need to validate that the certificate requestor owns the corresponding domains. AWS recommend validating domain
ownership through DNS. Follow the prompts to create the challenge records in route 53, and then wait for the certificate
to be available.

With the certificate taken care of, head back to the API Gateway console and create a custom domain name resource. Enter
`api-dev.example.company.org` for the domain name, and choose the matching certificate. Leave the endpoint type as regional.
After you've created the custom domain resource, you should map it to the api gateway stage. From the api list select
`example-backend-dev`, for the stage select `$default`, and leave the path empty. This mapping prepares all requests
to the custom domain to be handled by your HTTP api gateway. 

Under the endpoint configuration for the custom domain resource, take note of the generated domain name. It looks similar
to `d-0123456789.execute-api.us-east-1.amazonaws.com` Also, since you're using a custom domain there's no need for the
first generated url. You can disable that endpoint under the general config for the HTTP api.

Finally, head over to Route53 and review the DNS records for your domain's hosted zone, which is most likely `company.org`.
Create the new record with `api-dev.example` as the subdomain and the record type as `A`. We want to configure record as
an alias to another AWS service. This allows us to dynamically route traffic to API Gateway's ip addresses through the `d-`
endpoint that was generated for us. For the traffic routing options choose API Gateway and the region you've been working
with. Choose the endpoint that shows up in the dropdown and verify it matches the `d-` endpoint.

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
