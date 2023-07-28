from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ConfigDict, RootModel

from .object_id import PydanticObjectId


class Document(BaseModel):
    id: PydanticObjectId | str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_pymongo(cls, doc: dict) -> DocumentType:
        _id = doc.pop('_id')
        return cls(id=_id, **doc)

    @property
    def object_ref(self) -> ObjectRef[DocumentType]:
        return ObjectRef[DocumentType](__root__=self.id)


DocumentType = TypeVar('DocumentType', bound=Document)


class ObjectRef(RootModel[DocumentType]):
    root: PydanticObjectId | str
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def id(self):
        return self.root
