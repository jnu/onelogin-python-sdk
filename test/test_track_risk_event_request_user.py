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
from openapi_client.models.track_risk_event_request_user import TrackRiskEventRequestUser  # noqa: E501
from openapi_client.rest import ApiException

class TestTrackRiskEventRequestUser(unittest.TestCase):
    """TrackRiskEventRequestUser unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TrackRiskEventRequestUser
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TrackRiskEventRequestUser`
        """
        model = openapi_client.models.track_risk_event_request_user.TrackRiskEventRequestUser()  # noqa: E501
        if include_optional :
            return TrackRiskEventRequestUser(
                id = '', 
                name = '', 
                authenticated = True
            )
        else :
            return TrackRiskEventRequestUser(
                id = '',
        )
        """

    def testTrackRiskEventRequestUser(self):
        """Test TrackRiskEventRequestUser"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
