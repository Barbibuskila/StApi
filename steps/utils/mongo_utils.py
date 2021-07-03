from steps.common.base import MongoBaseModel
from typing import Dict


def convert_model_to_document(mongo_model: MongoBaseModel, with_id=False) -> Dict:
    """
    Convert specific MongoBaseModel to dictionary (document)
    :param mongo_model: Instance of specific MongoBaseModel
    :param with_id: Determined if to return id of the model
    :return: Document (dictionary)
    """
    return mongo_model.dict() if with_id else mongo_model.dict(exclude={"id"})
