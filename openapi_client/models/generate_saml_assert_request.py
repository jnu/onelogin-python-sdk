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
from pydantic import BaseModel, Field, StrictStr

class GenerateSamlAssertRequest(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    username_or_email: StrictStr = Field(..., description="Set this to the username or email of the OneLogin user accessing the app for which you want to generate a SAML token.")
    password: StrictStr = Field(..., description="Password of the OneLogin user accessing the app for which you want to generate a SAML token.")
    app_id: StrictStr = Field(..., description="App ID of the app for which you want to generate a SAML token. This is the app ID in OneLogin.")
    subdomain: StrictStr = Field(..., description="Set to the subdomain of the OneLogin user accessing the app for which you want to generate a SAML token.")
    ip_address: Optional[StrictStr] = Field(None, description="If you are using this API in a scenario in which MFA is required and you’ll need to be able to honor IP address whitelisting defined in MFA policies, provide this parameter and set its value to the whitelisted IP address that needs to be bypassed.")
    __properties = ["username_or_email", "password", "app_id", "subdomain", "ip_address"]

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
    def from_json(cls, json_str: str) -> GenerateSamlAssertRequest:
        """Create an instance of GenerateSamlAssertRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GenerateSamlAssertRequest:
        """Create an instance of GenerateSamlAssertRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GenerateSamlAssertRequest.parse_obj(obj)

        _obj = GenerateSamlAssertRequest.parse_obj({
            "username_or_email": obj.get("username_or_email"),
            "password": obj.get("password"),
            "app_id": obj.get("app_id"),
            "subdomain": obj.get("subdomain"),
            "ip_address": obj.get("ip_address")
        })
        return _obj

