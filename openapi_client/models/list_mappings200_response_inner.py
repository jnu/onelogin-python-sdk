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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, validator
from openapi_client.models.list_mappings200_response_inner_actions_inner import ListMappings200ResponseInnerActionsInner
from openapi_client.models.list_mappings200_response_inner_conditions_inner import ListMappings200ResponseInnerConditionsInner

class ListMappings200ResponseInner(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    id: Optional[StrictInt] = None
    name: StrictStr = Field(..., description="The name of the mapping.")
    enabled: StrictBool = Field(..., description="Indicates if the mapping is enabled or not.")
    match: StrictStr = Field(..., description="Indicates how conditions should be matched.")
    position: StrictInt = Field(..., description="Indicates the order of the mapping. When `null` this will default to last position.")
    conditions: List[ListMappings200ResponseInnerConditionsInner] = Field(..., description="An array of conditions that the user must meet in order for the mapping to be applied.")
    actions: List[ListMappings200ResponseInnerActionsInner] = Field(..., description="An array of actions that will be applied to the users that are matched by the conditions.")
    __properties = ["id", "name", "enabled", "match", "position", "conditions", "actions"]

    @validator('match')
    def match_validate_enum(cls, v):
        if v not in ('all', 'any'):
            raise ValueError("must validate the enum values ('all', 'any')")
        return v

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
    def from_json(cls, json_str: str) -> ListMappings200ResponseInner:
        """Create an instance of ListMappings200ResponseInner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in conditions (list)
        _items = []
        if self.conditions:
            for _item in self.conditions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['conditions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in actions (list)
        _items = []
        if self.actions:
            for _item in self.actions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['actions'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListMappings200ResponseInner:
        """Create an instance of ListMappings200ResponseInner from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListMappings200ResponseInner.parse_obj(obj)

        _obj = ListMappings200ResponseInner.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "enabled": obj.get("enabled"),
            "match": obj.get("match"),
            "position": obj.get("position"),
            "conditions": [ListMappings200ResponseInnerConditionsInner.from_dict(_item) for _item in obj.get("conditions")] if obj.get("conditions") is not None else None,
            "actions": [ListMappings200ResponseInnerActionsInner.from_dict(_item) for _item in obj.get("actions")] if obj.get("actions") is not None else None
        })
        return _obj

