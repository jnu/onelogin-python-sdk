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
from openapi_client.models.get_role_by_name200_response_pagination import GetRoleByName200ResponsePagination  # noqa: E501
from openapi_client.rest import ApiException

class TestGetRoleByName200ResponsePagination(unittest.TestCase):
    """GetRoleByName200ResponsePagination unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test GetRoleByName200ResponsePagination
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetRoleByName200ResponsePagination`
        """
        model = openapi_client.models.get_role_by_name200_response_pagination.GetRoleByName200ResponsePagination()  # noqa: E501
        if include_optional :
            return GetRoleByName200ResponsePagination(
                after_cursor = 'xWNjb3VudF9pZDo6OjUzNDEzLS0jI2lkOjo6OTA0MjU3NTQ2', 
                before_cursor = '""', 
                next_link = 'https://{subdomain}.onelogin.com/api/1/events?after_cursor=xWNjb3VudF9pZDo6OjUzNDEzLS0jI2lkOjo6OTA0MjU3NTQ2', 
                previous_link = '""'
            )
        else :
            return GetRoleByName200ResponsePagination(
        )
        """

    def testGetRoleByName200ResponsePagination(self):
        """Test GetRoleByName200ResponsePagination"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
