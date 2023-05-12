from typing import Generic

from pydantic.generics import BaseModel, GenericModel

from ...model.document import DocumentType


class CreateResponse(GenericModel, Generic[DocumentType]):
    __root__: DocumentType


class ReadResponse(GenericModel, Generic[DocumentType]):
    __root__: DocumentType


class UpdateResponse(GenericModel, Generic[DocumentType]):
    __root__: DocumentType


class DeleteResponse(GenericModel, Generic[DocumentType]):
    data: DocumentType
    acknowledged: bool


class ListResponse(GenericModel, Generic[DocumentType]):
    data: list[DocumentType]


class PaginationMetadata(BaseModel):
    limit: int
    offset: int
    filter: dict | None


class PaginationResponse(GenericModel, Generic[DocumentType]):
    data: list[DocumentType]
    count: int
    total_count: int
    has_more: bool
    meta: PaginationMetadata
