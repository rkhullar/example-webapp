# FastAPI on AWS with MongoDB Atlas and Okta - Part 2

## Project Setup
### Virtual Environment
At the time of this writing the aws lambda runtime runs with python `3.10.9`. You can use a program like [`asdf`](https://asdf-vm.com)
to manage multiple versions of developer tools. In your project workspace use the following commands to create a virtual
environment and install the required libraries. As you add dependencies with `pipenv` they will be tracked with a `Pipfile`.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=venv.sh

### File Tree
Within the project workspace we will create the following structure:
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
|   `-- schema
|       |-- __init__.py
|       |-- message.py
|       `-- user.py
|-- lambda_function.py
`-- server.py
```

This structure wraps almost of all the fastapi logic into the `api` package. The `server` module should be used for local
development or containerized deployments, and the `lambda_function` module will be used in our AWS lambda deployment. The
idea behind `model` `routes` and `schema` being packages is to keep the project well organized as it expands with new
features. Each top level data resource would be defined under `model`, the routes to manage that data model would be under
`routes`, and the request and response schema for those routes would be under `schema`.

## Local Development

To start local development we will focus on the following four modules: `config` `router` `factory` `server`.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=config.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=router-v1.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=factory.py
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=server.py

At this point when you start up the application with `python server.py` you would see errors around missing environment
variables. I suggest using [`direnv`](https://direnv.net) with an `.envrc` and `local.env` files to manage that config for
local development. Direnv lets us modify the shell configuration based on the current working directory. And the
[IntelliJ IDE](https://www.jetbrains.com/idea) has plugins that work well with dot env files. By using both tools we can
define the config once and make it available for both the shell and IDE.

- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=.envrc.dist
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=local.env.dist
- https://gist.github.com/rkhullar/5f47b00b9d90edc3ae81702246d93dc7?file=local-dev.env.dist

Now when you start the local fastapi server and head over to `http://localhost:8000/docs` you should see an OpenAPI page
with one hello world route, and you should be able to try it out and get a successful response.


### Okta Integration (Revisit)
After you've created the client app take note of the "Client ID". That value should be used for the `OKTA_CLIENT_ID` in your
fastapi run configuration. You should also update the value for the `OKTA_HOST` if you haven't already. The default value
would be something like `dev-12345678.okta.com`.
