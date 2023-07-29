from typing import Annotated

from bson.objectid import ObjectId as BsonObjectId
from pydantic import GetPydanticSchema, PlainSerializer, WithJsonSchema
from pydantic_core import core_schema

# https://stackoverflow.com/questions/76686888/using-bson-objectid-in-p
# https://docs.pydantic.dev/dev-v2/usage/types/custom/#using-getpydanticschema-to-reduce-boilerplate

# NOTE: only export supported currently
PydanticObjectId = Annotated[
    BsonObjectId,
    GetPydanticSchema(lambda source_type, handler: core_schema.is_instance_schema(BsonObjectId)),
    PlainSerializer(lambda data: str(data), return_type=str),
    WithJsonSchema({'type': 'string', 'example': 'ObjectId()'})
]

'''
# NOTE: deprecated for pydantic 2
class PydanticObjectId(BsonObjectId):
    # https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, BsonObjectId):
            raise TypeError('ObjectId required')
        return value

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string', example='ObjectId()')

    @classmethod
    def register(cls):
        from pydantic.v1.json import ENCODERS_BY_TYPE
        ENCODERS_BY_TYPE[BsonObjectId] = str


PydanticObjectId.register()
'''
