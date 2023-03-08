from typing import TypeVar, Union

from bson.objectid import ObjectId
from pydantic import BaseModel

from .object_id import PydanticObjectId

DocumentType = TypeVar('DocumentType', bound='Document')


class Document(BaseModel):
    # TODO: try to preserve original id type
    id: Union[PydanticObjectId, str]  # NOTE: only string after instantiation

    @classmethod
    def from_pymongo(cls, doc: dict) -> DocumentType:
        _id = doc.pop('_id')
        return cls(id=_id, **doc)

    @property
    def object_id(self) -> ObjectId:
        return ObjectId(self.id)
