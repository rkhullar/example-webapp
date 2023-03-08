from bson.objectid import ObjectId as BsonObjectId


class PydanticObjectId(BsonObjectId):
    # https://stackoverflow.com/questions/59503461/how-to-parse-objectid-in-a-pydantic-model

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string', example='ObjectId()')
