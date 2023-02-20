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
from openapi_client.models.create_message_template_request_template_one_of1 import CreateMessageTemplateRequestTemplateOneOf1  # noqa: E501
from openapi_client.rest import ApiException

class TestCreateMessageTemplateRequestTemplateOneOf1(unittest.TestCase):
    """CreateMessageTemplateRequestTemplateOneOf1 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test CreateMessageTemplateRequestTemplateOneOf1
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateMessageTemplateRequestTemplateOneOf1`
        """
        model = openapi_client.models.create_message_template_request_template_one_of1.CreateMessageTemplateRequestTemplateOneOf1()  # noqa: E501
        if include_optional :
            return CreateMessageTemplateRequestTemplateOneOf1(
                message = 'Here is the code: {{otp_code}}'
            )
        else :
            return CreateMessageTemplateRequestTemplateOneOf1(
                message = 'Here is the code: {{otp_code}}',
        )
        """

    def testCreateMessageTemplateRequestTemplateOneOf1(self):
        """Test CreateMessageTemplateRequestTemplateOneOf1"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
