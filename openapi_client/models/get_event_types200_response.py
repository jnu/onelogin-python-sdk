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


from typing import List, Optional
from pydantic import BaseModel
from openapi_client.models.generate_token400_response import GenerateToken400Response
from openapi_client.models.get_event_types200_response_data_inner import GetEventTypes200ResponseDataInner

class GetEventTypes200Response(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    status: Optional[GenerateToken400Response] = None
    data: Optional[List[GetEventTypes200ResponseDataInner]] = None
    __properties = ["status", "data"]

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
    def from_json(cls, json_str: str) -> GetEventTypes200Response:
        """Create an instance of GetEventTypes200Response from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of status
        if self.status:
            _dict['status'] = self.status.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in data (list)
        _items = []
        if self.data:
            for _item in self.data:
                if _item:
                    _items.append(_item.to_dict())
            _dict['data'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GetEventTypes200Response:
        """Create an instance of GetEventTypes200Response from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GetEventTypes200Response.parse_obj(obj)

        _obj = GetEventTypes200Response.parse_obj({
            "status": GenerateToken400Response.from_dict(obj.get("status")) if obj.get("status") is not None else None,
            "data": [GetEventTypes200ResponseDataInner.from_dict(_item) for _item in obj.get("data")] if obj.get("data") is not None else None
        })
        return _obj

