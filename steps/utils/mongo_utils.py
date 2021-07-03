from typing import Dict, Callable, Union

from pydantic import BaseModel

from steps.common.base import MongoBaseModel


def convert_model_to_document(mongo_model: MongoBaseModel, with_id=False) -> Dict:
    """
    Convert specific MongoBaseModel to dictionary (document)
    :param mongo_model: Instance of specific MongoBaseModel
    :param with_id: Determined if to return id of the model
    :return: Document (dictionary)
    """
    return mongo_model.dict() if with_id else mongo_model.dict(exclude={"id"})


def convert_document_to_model(document: Dict, mongo_model_cls: Callable) -> Union[BaseModel, MongoBaseModel]:
    """
    Convert document dictionary to the given model by using its constructor
    :param document: Dictionary that contains all keys of the models
    :param mongo_model_cls: Specific BaseModel class
    :return: Instance of specific BaseModel
    """
    return mongo_model_cls(**document)
