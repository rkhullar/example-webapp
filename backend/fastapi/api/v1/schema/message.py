import datetime as dt

from pydantic import BaseModel, constr


class CreateMessage(BaseModel):
    message: constr(strip_whitespace=False, min_length=3)

    def to_pymongo(self, okta_id: str) -> dict:
        return dict(created=dt.datetime.utcnow(), okta_id=okta_id, message=self.message)
