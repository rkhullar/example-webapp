from typing import Generic

from pydantic import BaseModel, RootModel

from ...model.document import DocumentType


class CreateResponse(RootModel[DocumentType], Generic[DocumentType]):
    root: DocumentType


class ReadResponse(RootModel[DocumentType], Generic[DocumentType]):
    root: DocumentType


class UpdateResponse(RootModel[DocumentType], Generic[DocumentType]):
    root: DocumentType


class DeleteResponse(BaseModel, Generic[DocumentType]):
    data: DocumentType
    acknowledged: bool


class ListResponse(BaseModel, Generic[DocumentType]):
    data: list[DocumentType]


class PaginationMetadata(BaseModel):
    limit: int
    offset: int
    filter: dict | None


class PaginationResponse(BaseModel, Generic[DocumentType]):
    data: list[DocumentType]
    count: int
    total_count: int
    has_more: bool
    meta: PaginationMetadata
