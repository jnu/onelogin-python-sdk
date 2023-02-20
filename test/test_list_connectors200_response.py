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
from openapi_client.models.list_connectors200_response import ListConnectors200Response  # noqa: E501
from openapi_client.rest import ApiException

class TestListConnectors200Response(unittest.TestCase):
    """ListConnectors200Response unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ListConnectors200Response
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ListConnectors200Response`
        """
        model = openapi_client.models.list_connectors200_response.ListConnectors200Response()  # noqa: E501
        if include_optional :
            return ListConnectors200Response(
                id = 1061937, 
                name = 'Amazon Web Services Multi-Role', 
                icon_url = 'https://cdn-shadow.onlgn.net/images/icons/square/amazonwebservices3multirole/old_original.png?1421095823', 
                auth_method = 2, 
                allows_new_parameters = True
            )
        else :
            return ListConnectors200Response(
        )
        """

    def testListConnectors200Response(self):
        """Test ListConnectors200Response"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
