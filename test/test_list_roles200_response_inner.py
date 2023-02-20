# coding: utf-8

"""
    OneLogin API

    OpenAPI Specification for OneLogin  # noqa: E501

    The version of the OpenAPI document: 3.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import openapi_client
from openapi_client.models.list_roles200_response_inner import ListRoles200ResponseInner  # noqa: E501
from openapi_client.rest import ApiException

class TestListRoles200ResponseInner(unittest.TestCase):
    """ListRoles200ResponseInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListRoles200ResponseInner
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListRoles200ResponseInner`
        """
        model = openapi_client.models.list_roles200_response_inner.ListRoles200ResponseInner()  # noqa: E501
        if include_optional :
            return ListRoles200ResponseInner(
                id = 56, 
                name = '', 
                apps = [
                    56
                    ], 
                users = [
                    56
                    ], 
                admins = [
                    56
                    ]
            )
        else :
            return ListRoles200ResponseInner(
                name = '',
        )
        """

    def testListRoles200ResponseInner(self):
        """Test ListRoles200ResponseInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
