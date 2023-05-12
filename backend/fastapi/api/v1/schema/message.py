import datetime as dt

from pydantic import BaseModel, constr


class CreateMessage(BaseModel):
    message: constr(strip_whitespace=False, min_length=3)

    def to_pymongo(self, user_id: str) -> dict:
        return dict(created=dt.datetime.utcnow(), user_id=user_id, message=self.message)
