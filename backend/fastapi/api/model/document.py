from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from .object_id import PydanticObjectId


class Document(BaseModel):
    id: PydanticObjectId | str

    @classmethod
    def from_pymongo(cls, doc: dict) -> DocumentType:
        _id = doc.pop('_id')
        return cls(id=_id, **doc)

    @property
    def object_ref(self) -> ObjectRef[DocumentType]:
        return ObjectRef[DocumentType](__root__=self.id)


DocumentType = TypeVar('DocumentType', bound=Document)


class ObjectRef(GenericModel, Generic[DocumentType]):
    # TODO: try field alias
    __root__: PydanticObjectId | str

    @property
    def id(self):
        return self.__root__
