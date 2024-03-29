# FastAPI on AWS with MongoDB Atlas and Okta - Part 2
## Project Setup and Local Development

### Virtual Environment
In July 2023 the latest AWS lambda runtime version is `Python 3.11`. You can use a program like [`asdf`][asdf] to manage multiple
versions of developer tools. In your project workspace use the following commands to create a virtual environment and install
the required libraries. As you add dependencies with `pipenv` they will be tracked with a `Pipfile`.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=venv.sh

### File Tree
Within the project workspace we will create the below file structure. The `__init__.py` files are all empty and just
mark the containing folder as a python package.
```text
|-- api
|   |-- __init__.py
|   |-- config.py
|   |-- depends.py
|   |-- factory.py
|   |-- model
|   |   |-- __init__.py
|   |   |-- document.py
|   |   |-- message.py
|   |   `-- object_id.py
|   |-- router.py
|   |-- routes
|   |   |-- __init__.py
|   |   `-- message.py
|   |-- schema
|   |   |-- __init__.py
|   |   |-- crud.py
|   |   |-- message.py
|   |   `-- user.py
|   `-- util
|       |-- __init__.py
|       `-- okta_flow.py
|-- lambda_function.py
`-- server.py
```

This structure wraps almost of all the fastapi logic into the `api` package. The `server` module should be used for local
development or containerized deployments, and the `lambda_function` module will be used in our AWS lambda deployment. The
idea behind `model` `routes` and `schema` being packages is to keep the project well organized as it expands with new
features. Each top level data resource would be defined under `model`, the routes to manage that data model would be under
`routes`, and the request and response schema for those routes would be under `schema`.

### Hello World

To start local development we will focus on the following four modules: `config` `router` `factory` `server`.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=config.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-root-v1.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=factory-v1.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=server.py

At this point when you start up the application with `python server.py` you would see errors around missing environment
variables. I suggest using [`direnv`][direnv] with `.envrc` and `local.env` files to manage that config for local development.
Direnv lets us modify the shell configuration based on the current working directory. And the [IntelliJ IDE][intellij] has
plugins that work well with dot env files. By using both tools we can define the config once and make it available for both
the shell and IDE.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=.envrc.dist
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=local.env.dist
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=local-dev.env.dist

Now when you start the local fastapi server and head over to `http://localhost:8000/docs` you should see an OpenAPI page
with one hello world route, and you should be able to try it out and get a successful response.

There should also be an`Authorize` button on the page. Since we've already included the `swagger_ui` settings in the factory
function, you don't need to enter any config when you authorize. There's no client secret because we created the client in
okta as Single Page App (SPA), which uses Proof Key for Code Exchange (PKCE). So the auth flow from the docs should take
your okta hosted login, and after you authenticate there, it should redirect you back to the docs to complete the flow.

### Okta Integration
Next we need to protect the backend endpoints by requiring user authentication. We could use the `OAuth2AuthorizationCodeBearer`
directly under `fastapi.security`, but I like to extend that class with logic tailored to the authentication service provider.
The custom `OktaAuthCodeBearer` defined below takes in the okta host and optionally the issuer id, builds the OIDC
metadata endpoint, and loads the authorization and token urls into the parent constructor.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=okta-flow.py

Let's instantiate the class within our `depends` module so that it can be reused across multiple routers with the api.
In the auth flow when users authenticate on the browser they receive an access token from Okta. In order to read user
profile information or setup role based access control, we need to use the access token to call the user info endpoint.
The resulting identity token should contain the claims configured for your okta authorization server, including the user's
profile name.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=schema-user.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=depends-v1-okta.py

Now we can update our hello world endpoint. The `GetUser` annotation allows us to include the `get_user` dependency to the
route handler function in a concise way. And that's useful since each function that needs access to user information would
need the `user` parameter. Without the annotation that parameter would be `user: User = Depends(get_user)`.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-root-v2-okta.py

### MongoDB Integration
For our database integrations we're going to create an instance of the pymongo `MongoClient` within our factory function.
Then we'll create another annotated dependency function so that we can easily grab pymongo `Collection` objects as needed
within our route handlers.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=factory-v2-atlas.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=depends-v2-atlas-delta.py

Now we can start implementing the endpoints for users to create and read their messages in the collection. We'll update the
root router module and remove the hello world endpoint. We'll define the schema for parsing the json payload when creating
new messages.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-root-v3.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=schema-message.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-message-v1.py

At this point you should be able to test both endpoints from the openapi docs. If you are testing with more than one user,
you'll notice that each user can only read messages that they've posted. In the query within the list messages endpoint,
we are filtering for documents based on the user's okta id. However, the query needs to be optimized by adding an index on
the collection. Check out the MongoDB docs to learn how to create collection indexes [[link][atlas-index-docs]]. For the
example project I created two indexes; `{"user_id": "hashed"}` and `{"created": -1}`

### Database Models and Response Schemas
With the integrations now working we can improve the generated openapi docs by defining response schemas. For example, the
endpoint to read messages should return a list of `Message` documents. We'll create some helper modules to define generic
crud responses and the base class for data models. You may also want to look at two other libraries for defining data models:
[mongoengine][mongoengine-pypi] and [beanie][beanie-pypi]

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=model-document.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=model-object-id.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=schema-crud.py

Now we can define the data model for messages, and update the router.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=model-message.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-message-v2.py

---
- [Continue to Part 3: Deploying to API Gateway and Lambda][part-3]
- [Overview][overview]

[asdf]: https://asdf-vm.com
[direnv]: https://direnv.net
[intellij]: https://www.jetbrains.com/idea
[atlas-index-docs]: https://www.mongodb.com/docs/atlas/atlas-ui/indexes
[mongoengine-pypi]: https://pypi.org/project/mongoengine
[beanie-pypi]: https://pypi.org/project/beanie
