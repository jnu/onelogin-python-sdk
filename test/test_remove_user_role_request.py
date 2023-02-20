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
from openapi_client.models.remove_user_role_request import RemoveUserRoleRequest  # noqa: E501
from openapi_client.rest import ApiException

class TestRemoveUserRoleRequest(unittest.TestCase):
    """RemoveUserRoleRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RemoveUserRoleRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RemoveUserRoleRequest`
        """
        model = openapi_client.models.remove_user_role_request.RemoveUserRoleRequest()  # noqa: E501
        if include_optional :
            return RemoveUserRoleRequest(
                role_id_array = [
                    openapi_client.models.remove_user_role_request_role_id_array_inner.removeUserRole_request_role_id_array_inner(
                        role_id = 56, )
                    ]
            )
        else :
            return RemoveUserRoleRequest(
                role_id_array = [
                    openapi_client.models.remove_user_role_request_role_id_array_inner.removeUserRole_request_role_id_array_inner(
                        role_id = 56, )
                    ],
        )
        """

    def testRemoveUserRoleRequest(self):
        """Test RemoveUserRoleRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
