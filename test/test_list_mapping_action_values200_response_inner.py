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
from openapi_client.models.list_mapping_action_values200_response_inner import ListMappingActionValues200ResponseInner  # noqa: E501
from openapi_client.rest import ApiException

class TestListMappingActionValues200ResponseInner(unittest.TestCase):
    """ListMappingActionValues200ResponseInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListMappingActionValues200ResponseInner
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListMappingActionValues200ResponseInner`
        """
        model = openapi_client.models.list_mapping_action_values200_response_inner.ListMappingActionValues200ResponseInner()  # noqa: E501
        if include_optional :
            return ListMappingActionValues200ResponseInner(
                name = 'default', 
                value = 199848
            )
        else :
            return ListMappingActionValues200ResponseInner(
        )
        """

    def testListMappingActionValues200ResponseInner(self):
        """Test ListMappingActionValues200ResponseInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
