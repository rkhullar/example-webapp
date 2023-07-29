from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field, RootModel

from .object_id import PydanticObjectId


class Document(BaseModel):
    id: PydanticObjectId | str = Field(alias='_id')

    @classmethod
    def from_pymongo(cls, doc: dict) -> DocumentType:
        # _id = doc.pop('_id')
        # return cls(id=_id, **doc)
        return cls(**doc)

    @property
    def object_ref(self) -> ObjectRef[DocumentType]:
        return ObjectRef[DocumentType](__root__=self.id)


DocumentType = TypeVar('DocumentType', bound=Document)


class ObjectRef(RootModel[DocumentType], Generic[DocumentType]):
    root: PydanticObjectId | str

    @property
    def id(self):
        return self.root
