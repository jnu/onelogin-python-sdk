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


from typing import Optional
from pydantic import BaseModel, StrictStr
from openapi_client.models.list_priveleges200_response_inner_privilege import ListPriveleges200ResponseInnerPrivilege

class ListPriveleges200ResponseInner(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    id: Optional[StrictStr] = None
    name: StrictStr = ...
    description: Optional[StrictStr] = None
    privilege: ListPriveleges200ResponseInnerPrivilege = ...
    __properties = ["id", "name", "description", "privilege"]

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
    def from_json(cls, json_str: str) -> ListPriveleges200ResponseInner:
        """Create an instance of ListPriveleges200ResponseInner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of privilege
        if self.privilege:
            _dict['privilege'] = self.privilege.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListPriveleges200ResponseInner:
        """Create an instance of ListPriveleges200ResponseInner from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListPriveleges200ResponseInner.parse_obj(obj)

        _obj = ListPriveleges200ResponseInner.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "privilege": ListPriveleges200ResponseInnerPrivilege.from_dict(obj.get("privilege")) if obj.get("privilege") is not None else None
        })
        return _obj

