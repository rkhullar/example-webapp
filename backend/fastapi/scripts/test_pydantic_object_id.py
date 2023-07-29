from unittest import TestCase

from bson import ObjectId
from model.object_id import PydanticObjectId
from pydantic import BaseModel, Field


class ExampleModel(BaseModel):
    # NOTE: only export is supported
    id: PydanticObjectId = Field(alias='_id')


class PydanticObjectIdTest(TestCase):

    def test_init(self):
        _id = ObjectId()
        result = PydanticObjectId(_id)
        self.assertEqual(result, _id)

    def test_model_export(self):
        _id = ObjectId()
        dut = ExampleModel(_id=_id)
        exported = dut.model_dump()
        expected = {'id': str(_id)}
        self.assertEqual(exported, expected)
