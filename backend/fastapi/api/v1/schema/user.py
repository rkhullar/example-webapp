from pydantic import BaseModel


class OktaIdentityToken(BaseModel):
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
    id: str
    name: str
    email: str
    groups: set[str]


class OktaUser(User):

    @classmethod
    def from_token(cls, token: OktaIdentityToken) -> 'OktaUser':
        return cls(id=token.sub, name=token.name, email=token.email, groups=token.groups)
