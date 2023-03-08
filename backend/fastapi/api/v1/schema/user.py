from pydantic import BaseModel


class IdentityToken(BaseModel):
    sub: str
    name: str
    locale: str
    email: str
    preferred_username: str
    given_name: str
    family_name: str
    zoneinfo: str
    email_verified: bool
    groups: list[str]


class User(BaseModel):
    okta_id: str
    name: str
    email: str
    groups: set[str]

    @classmethod
    def from_token(cls, token: IdentityToken) -> 'User':
        return cls(okta_id=token.sub, name=token.name, email=token.email, groups=token.groups)
