from typing import Optional

from bson import ObjectId
from pydantic import BaseModel as _BaseModel, Field


class PyObjectId(ObjectId):
    """
    Custom ObjectId For pydantic to handle it
    """

    @classmethod
    def __get_validators__(cls):
        """
        Access to class validators
        :return: Validators
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate object id
        :param v: object id representation
        :return: ObjectId with a valid value
        """
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """
        Update the schema to string for pydantic
        :param field_schema: current field schema
        :return:
        """
        field_schema.update(type='string')


class MongoBaseModel(_BaseModel):
    """
    id: MongoDb ObjectId
    """
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
