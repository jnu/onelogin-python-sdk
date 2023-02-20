# coding: utf-8

"""
    OneLogin API

    OpenAPI Specification for OneLogin  # noqa: E501

    The version of the OpenAPI document: 3.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json



from pydantic import BaseModel, Field, StrictStr

class CreateMessageTemplateRequestTemplateOneOfAllOf(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    subject: StrictStr = Field(..., description="Custom Email Subject")
    html: StrictStr = Field(..., description="The HTML body of the Custom Email")
    plain: StrictStr = Field(..., description="The Plain text body of the email")
    __properties = ["subject", "html", "plain"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> CreateMessageTemplateRequestTemplateOneOfAllOf:
        """Create an instance of CreateMessageTemplateRequestTemplateOneOfAllOf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateMessageTemplateRequestTemplateOneOfAllOf:
        """Create an instance of CreateMessageTemplateRequestTemplateOneOfAllOf from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return CreateMessageTemplateRequestTemplateOneOfAllOf.parse_obj(obj)

        _obj = CreateMessageTemplateRequestTemplateOneOfAllOf.parse_obj({
            "subject": obj.get("subject"),
            "html": obj.get("html"),
            "plain": obj.get("plain")
        })
        return _obj

