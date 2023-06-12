```mermaid
sequenceDiagram
Caller->>Okta: submit credentials
Okta->>Caller: return JWT access token
Caller->>HTTP API: send request with JWT
Okta->>HTTP API: serve public keys
HTTP API->>Lambda: invoke lambda
Lambda->>FastAPI: handle request
FastAPI->>MongoDB Atlas: read or write data
```
