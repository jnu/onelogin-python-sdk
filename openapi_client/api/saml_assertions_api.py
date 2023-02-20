# coding: utf-8

"""
    OneLogin API

    OpenAPI Specification for OneLogin  # noqa: E501

    The version of the OpenAPI document: 3.1.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

from pydantic import validate_arguments, ValidationError
from typing_extensions import Annotated

from pydantic import StrictStr

from typing import Optional

from openapi_client.models.generate_saml_assert200_response import GenerateSamlAssert200Response
from openapi_client.models.generate_saml_assert_request import GenerateSamlAssertRequest
from openapi_client.models.ver_factor_saml200_response import VerFactorSaml200Response
from openapi_client.models.ver_factor_saml_request import VerFactorSamlRequest

from openapi_client.api_client import ApiClient
from openapi_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class SAMLAssertionsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient.get_default()
        self.api_client = api_client

    @validate_arguments
    def generate_saml_assert(self, content_type : Optional[StrictStr] = None, generate_saml_assert_request : Optional[GenerateSamlAssertRequest] = None, **kwargs) -> GenerateSamlAssert200Response:  # noqa: E501
        """Generate SAML Assertion  # noqa: E501

        Generate SAML Assertion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.generate_saml_assert(content_type, generate_saml_assert_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param generate_saml_assert_request:
        :type generate_saml_assert_request: GenerateSamlAssertRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GenerateSamlAssert200Response
        """
        kwargs['_return_http_data_only'] = True
        return self.generate_saml_assert_with_http_info(content_type, generate_saml_assert_request, **kwargs)  # noqa: E501

    @validate_arguments
    def generate_saml_assert_with_http_info(self, content_type : Optional[StrictStr] = None, generate_saml_assert_request : Optional[GenerateSamlAssertRequest] = None, **kwargs):  # noqa: E501
        """Generate SAML Assertion  # noqa: E501

        Generate SAML Assertion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.generate_saml_assert_with_http_info(content_type, generate_saml_assert_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param generate_saml_assert_request:
        :type generate_saml_assert_request: GenerateSamlAssertRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GenerateSamlAssert200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'content_type',
            'generate_saml_assert_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method generate_saml_assert" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        if _params['content_type']:
            _header_params['Content-Type'] = _params['content_type']

        # process the form parameters
        _form_params = []
        _files = {}

        # process the body parameter
        _body_params = None
        if _params['generate_saml_assert_request']:
            _body_params = _params['generate_saml_assert_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['OAuth2']  # noqa: E501

        _response_types_map = {
            '200': "GenerateSamlAssert200Response",
            '400': "GenerateToken400Response",
            '401': "GenerateToken400Response",
        }

        return self.api_client.call_api(
            '/api/1/saml_assertion', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def generate_saml_assert2(self, content_type : Optional[StrictStr] = None, generate_saml_assert_request : Optional[GenerateSamlAssertRequest] = None, **kwargs) -> GenerateSamlAssert200Response:  # noqa: E501
        """Generate SAML Assertion  # noqa: E501

        Generate SAML Assertion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.generate_saml_assert2(content_type, generate_saml_assert_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param generate_saml_assert_request:
        :type generate_saml_assert_request: GenerateSamlAssertRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: GenerateSamlAssert200Response
        """
        kwargs['_return_http_data_only'] = True
        return self.generate_saml_assert2_with_http_info(content_type, generate_saml_assert_request, **kwargs)  # noqa: E501

    @validate_arguments
    def generate_saml_assert2_with_http_info(self, content_type : Optional[StrictStr] = None, generate_saml_assert_request : Optional[GenerateSamlAssertRequest] = None, **kwargs):  # noqa: E501
        """Generate SAML Assertion  # noqa: E501

        Generate SAML Assertion  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.generate_saml_assert2_with_http_info(content_type, generate_saml_assert_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param generate_saml_assert_request:
        :type generate_saml_assert_request: GenerateSamlAssertRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(GenerateSamlAssert200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'content_type',
            'generate_saml_assert_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method generate_saml_assert2" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        if _params['content_type']:
            _header_params['Content-Type'] = _params['content_type']

        # process the form parameters
        _form_params = []
        _files = {}

        # process the body parameter
        _body_params = None
        if _params['generate_saml_assert_request']:
            _body_params = _params['generate_saml_assert_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['OAuth2']  # noqa: E501

        _response_types_map = {
            '200': "GenerateSamlAssert200Response",
            '400': "GenerateToken400Response",
            '401': "GenerateToken400Response",
        }

        return self.api_client.call_api(
            '/api/2/saml_assertion', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def ver_factor_saml(self, content_type : Optional[StrictStr] = None, ver_factor_saml_request : Optional[VerFactorSamlRequest] = None, **kwargs) -> VerFactorSaml200Response:  # noqa: E501
        """Verify Factor SAML  # noqa: E501

        Verify Factor: SAML  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.ver_factor_saml(content_type, ver_factor_saml_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param ver_factor_saml_request:
        :type ver_factor_saml_request: VerFactorSamlRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: VerFactorSaml200Response
        """
        kwargs['_return_http_data_only'] = True
        return self.ver_factor_saml_with_http_info(content_type, ver_factor_saml_request, **kwargs)  # noqa: E501

    @validate_arguments
    def ver_factor_saml_with_http_info(self, content_type : Optional[StrictStr] = None, ver_factor_saml_request : Optional[VerFactorSamlRequest] = None, **kwargs):  # noqa: E501
        """Verify Factor SAML  # noqa: E501

        Verify Factor: SAML  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.ver_factor_saml_with_http_info(content_type, ver_factor_saml_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param ver_factor_saml_request:
        :type ver_factor_saml_request: VerFactorSamlRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(VerFactorSaml200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'content_type',
            'ver_factor_saml_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ver_factor_saml" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        if _params['content_type']:
            _header_params['Content-Type'] = _params['content_type']

        # process the form parameters
        _form_params = []
        _files = {}

        # process the body parameter
        _body_params = None
        if _params['ver_factor_saml_request']:
            _body_params = _params['ver_factor_saml_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['OAuth2']  # noqa: E501

        _response_types_map = {
            '200': "VerFactorSaml200Response",
            '400': "GenerateToken400Response",
            '401': "GenerateToken400Response",
            '404': "GenerateToken400Response",
        }

        return self.api_client.call_api(
            '/api/1/saml_assertion/verify_factor', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))

    @validate_arguments
    def ver_factor_saml2(self, content_type : Optional[StrictStr] = None, ver_factor_saml_request : Optional[VerFactorSamlRequest] = None, **kwargs) -> VerFactorSaml200Response:  # noqa: E501
        """Verify Factor SAML  # noqa: E501

        Verify Factor: SAML  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.ver_factor_saml2(content_type, ver_factor_saml_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param ver_factor_saml_request:
        :type ver_factor_saml_request: VerFactorSamlRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: VerFactorSaml200Response
        """
        kwargs['_return_http_data_only'] = True
        return self.ver_factor_saml2_with_http_info(content_type, ver_factor_saml_request, **kwargs)  # noqa: E501

    @validate_arguments
    def ver_factor_saml2_with_http_info(self, content_type : Optional[StrictStr] = None, ver_factor_saml_request : Optional[VerFactorSamlRequest] = None, **kwargs):  # noqa: E501
        """Verify Factor SAML  # noqa: E501

        Verify Factor: SAML  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.ver_factor_saml2_with_http_info(content_type, ver_factor_saml_request, async_req=True)
        >>> result = thread.get()

        :param content_type:
        :type content_type: str
        :param ver_factor_saml_request:
        :type ver_factor_saml_request: VerFactorSamlRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :type _content_type: string, optional: force content-type for the request
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(VerFactorSaml200Response, status_code(int), headers(HTTPHeaderDict))
        """

        _params = locals()

        _all_params = [
            'content_type',
            'ver_factor_saml_request'
        ]
        _all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                '_content_type',
                '_headers'
            ]
        )

        # validate the arguments
        for _key, _val in _params['kwargs'].items():
            if _key not in _all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ver_factor_saml2" % _key
                )
            _params[_key] = _val
        del _params['kwargs']

        _collection_formats = {}

        # process the path parameters
        _path_params = {}

        # process the query parameters
        _query_params = []

        # process the header parameters
        _header_params = dict(_params.get('_headers', {}))
        if _params['content_type']:
            _header_params['Content-Type'] = _params['content_type']

        # process the form parameters
        _form_params = []
        _files = {}

        # process the body parameter
        _body_params = None
        if _params['ver_factor_saml_request']:
            _body_params = _params['ver_factor_saml_request']

        # set the HTTP header `Accept`
        _header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # set the HTTP header `Content-Type`
        _content_types_list = _params.get('_content_type',
            self.api_client.select_header_content_type(
                ['application/json']))
        if _content_types_list:
                _header_params['Content-Type'] = _content_types_list

        # authentication setting
        _auth_settings = ['OAuth2']  # noqa: E501

        _response_types_map = {
            '200': "VerFactorSaml200Response",
            '400': "GenerateToken400Response",
            '401': "GenerateToken400Response",
            '404': "GenerateToken400Response",
        }

        return self.api_client.call_api(
            '/api/2/saml_assertion/verify_factor', 'POST',
            _path_params,
            _query_params,
            _header_params,
            body=_body_params,
            post_params=_form_params,
            files=_files,
            response_types_map=_response_types_map,
            auth_settings=_auth_settings,
            async_req=_params.get('async_req'),
            _return_http_data_only=_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=_params.get('_preload_content', True),
            _request_timeout=_params.get('_request_timeout'),
            collection_formats=_collection_formats,
            _request_auth=_params.get('_request_auth'))
