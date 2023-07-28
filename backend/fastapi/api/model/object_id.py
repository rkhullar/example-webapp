from bson.objectid import ObjectId as BsonObjectId
from typing import Annotated
from pydantic import PlainSerializer, WithJsonSchema

# https://stackoverflow.com/questions/76686888/using-bson-objectid-in-p

PydanticObjectId = Annotated[
    BsonObjectId,
    PlainSerializer(lambda _id: str(_id), return_type=str),
    WithJsonSchema({'type': 'ObjectId()'}, mode='serialization')
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
