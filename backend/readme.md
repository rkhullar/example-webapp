#### Local Setup
```shell
asdf local python 3.10.9
./setup-dev.sh
```

#### Running Backend Locally
```shell
. backend/fastapi/venv/bin/activate
python backend/fastapi/server.py
```

#### Graphql Notes
- graphql url: http://localhost:8000/v1/graphql
- graphql example: [rkhullar/hello-edu/backend/fastapi/api/v1/router.py][graphql-router]

```text
# example query
query {
  books {title, author}
}
```

[graphql-router]: https://github.com/rkhullar/hello-edu/blob/main/backend/fastapi/api/v1/router.py
