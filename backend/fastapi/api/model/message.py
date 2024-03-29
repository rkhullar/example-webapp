import datetime as dt

from pydantic import Field

from .document import Document


class Message(Document):
    created: dt.datetime = Field(default_factory=dt.datetime.utcnow)
    user_id: str
    message: str
