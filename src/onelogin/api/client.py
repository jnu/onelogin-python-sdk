#!/usr/bin/python

""" OneLoginClient class

Copyright (c) 2017, OneLogin, Inc.
All rights reserved.

OneLoginClient class of the OneLogin's Python SDK.

"""

import datetime
from dateutil import tz
import requests
from defusedxml.lxml import fromstring

from onelogin.api.util.settings import Settings
from onelogin.api.util.constants import Constants
from onelogin.api.models.app import App
from onelogin.api.models.event import Event
from onelogin.api.models.event_type import EventType
from onelogin.api.models.group import Group
from onelogin.api.models.mfa import MFA
from onelogin.api.models.onelogin_token import OneLoginToken
from onelogin.api.models.rate_limit import RateLimit
from onelogin.api.models.role import Role
from onelogin.api.models.saml_endpoint_response import SAMLEndpointResponse
from onelogin.api.models.session_token_info import SessionTokenInfo
from onelogin.api.models.session_token_mfa_info import SessionTokenMFAInfo
from onelogin.api.models.user import User
from onelogin.api.version import __version__


class OneLoginClient(object):
    '''

    The OneLoginClient makes the API calls to the Onelogin's platform described
    at https://developers.onelogin.com/api-docs/1/getting-started/dev-overview.

    '''

    CUSTOM_USER_AGENT = "onelogin-python-sdk %s" % __version__

    def __init__(self, settings_path=None):
        """

        Create a new instance of OneLoginClient.

        :param path: Path where the sdk config file is located.
        :type path: string

        """
        self.settings = Settings(settings_path)
        self.user_agent = self.CUSTOM_USER_AGENT

    def clean_error(self):
        """

        Clean any previous error registered at the client.

        """
        self.error = None
        self.error_description = None

    def extract_error_message_from_response(self, response):
        message = ''
        content = response.json()
        if content and 'status' in content:
            status = content['status']
            if 'message' in status:
                message = status['message']
            elif 'type' in status:
                message = status['type']
        return message

    def get_after_cursor(self, response):
        after_cursor = None
        content = response.json()
        if content and 'pagination' in content and 'after_cursor' in content['pagination']:
            after_cursor = content['pagination']['after_cursor']
        return after_cursor

    def get_before_cursor(self, response):
        before_cursor = None
        content = response.json()
        if content and 'pagination' in content and 'before_cursor' in content['pagination']:
            before_cursor = content['pagination']['before_cursor']
        return before_cursor

    def handle_session_token_response(self, response):
        session_token = None
        content = response.json()
        if content and 'status' in content and 'message' in content['status'] and 'data' in content:
            if content['status']['message'] == "Success":
                session_token = SessionTokenInfo(content['data'][0])
            elif content['status']['message'] == "MFA is required for this user":
                session_token = SessionTokenMFAInfo(content['data'][0])
            else:
                raise Exception("Status Message type not reognized: %s" % content['status']['message'])
        return session_token

    def handle_saml_endpoint_response(self, response):
        saml_endpoint_response = None
        try:
            content = response.json()
            if content and 'status' in content and 'data' in content and 'message' in content['status'] and 'type' in content['status']:
                status_type = content['status']['type']
                status_message = content['status']['message']
                saml_endpoint_response = SAMLEndpointResponse(status_type, status_message)
                if status_message == 'Success':
                    saml_endpoint_response.saml_response = content['data']
                else:
                    mfa = MFA(content['data'][0])
                    saml_endpoint_response.mfa = mfa
        except:
            pass
        return saml_endpoint_response

    def handle_operation_response(self, response):
        result = False
        try:
            content = response.json()
            if content and 'status' in content and 'type' in content['status'] and content['status']['type'] == "success":
                result = True
        except:
            pass
        return result

    def retrieve_apps_from_xml(self, xml_content):
        root = fromstring(xml_content)
        node_list = root.xpath("/apps/app")
        attributes = ["id", "icon", "name", "provisioned", "extension_required", "personal", "login_id"]
        apps = []
        for node in node_list:
            app_data = {}
            for children in node.getchildren():
                if children.tag in attributes:
                    app_data[children.tag] = children.text
            apps.append(App(app_data))
        return apps

    def is_expired(self):
        return datetime.datetime.now(tz.tzutc()) > self.expiration

    def prepare_token(self):
        if self.access_token is None:
            self.get_access_token()
        elif self.is_expired():
            self.regenerate_token()

    def get_authorization(self, bearer=True):
        if bearer:
            authorization = "bearer:%s" % self.access_token
        else:
            authorization = "client_id:%s,client_secret:%s" % (self.settings.client_id, self.settings.client_secret)
        return authorization

    # OAuth 2.0 Tokens Methods
    def get_access_token(self):
        """

        Generates an access token and refresh token that you may use to
        call Onelogin's API methods.

        Returns the generated OAuth Token info
        :return: OAuth Token info
        :rtype: OneLoginToken object

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/generate-tokens Generate Tokens documentation.

        """
        self.clean_error()

        try:
            url = self.settings.get_url(Constants.TOKEN_REQUEST_URL)
            authorization = self.get_authorization(bearer=False)

            data = {
                'grant_type': 'client_credentials'
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    token = OneLoginToken(json_data['data'][0])
                    self.access_token = token.access_token
                    self.refresh_token = token.refresh_token
                    self.expiration = token.created_at + datetime.timedelta(seconds=token.expires_in)
                    return token
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def regenerate_token(self):
        """

        Refreshing tokens provides a new set of access and refresh tokens.

        Returns the refreshed OAuth Token info
        :return: OAuth Token info
        :rtype: OneLoginToken object

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/refresh-tokens Refresh Tokens documentation

        """
        self.clean_error()

        try:
            url = self.settings.get_url(Constants.TOKEN_REQUEST_URL)

            data = {
                'grant_type': 'refresh_token',
                'access_token': self.access_token,
                'refresh_token': self.refresh_token
            }

            headers = {
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    token = OneLoginToken(json_data['data'][0])
                    self.access_token = token.access_token
                    self.refresh_token = token.refresh_token
                    self.expiration = token.created_at + datetime.timedelta(seconds=token.expires_in)
                    return token
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def revoke_token(self):
        """

        Revokes an access token and refresh token pair.

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/revoke-tokens Revoke Tokens documentation

        """
        self.clean_error()

        try:
            url = self.settings.get_url(Constants.TOKEN_REVOKE_URL)
            authorization = self.get_authorization(bearer=False)

            data = {
                'access_token': self.access_token,
            }

            headers = {
                'Authorization': authorization,
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                self.access_token = None
                self.refresh_token = None
                self.expiration = None
                return True
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
                return False
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]
            return False

    def get_rate_limits(self):
        """

        Gets current rate limit details about an access token.

        Returns the rate limit info
        :return: rate limit info
        :rtype: RateLimit object

        See https://developers.onelogin.com/api-docs/1/oauth20-tokens/get-rate-limit Get Rate Limit documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_RATE_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    rate_limit = RateLimit(json_data['data'])
                    return rate_limit
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # User Methods
    def get_users(self, query_parameters=None):
        """

        Gets a list of User resources. (if no limit provided, by default gt 50 elements)

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        Returns the list of users
        :return: users list
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/users/get-users Get Users documentation

        """
        self.clean_error()
        self.prepare_token()
        limit = 50

        if query_parameters:
            if query_parameters.get('limit', None):
                limit = int(query_parameters.get('limit'))
                if limit > 50:
                    del query_parameters['limit']

        try:
            url = self.settings.get_url(Constants.GET_USERS_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            users = []
            response = None
            after_cursor = None
            while (not response) or (len(users) > limit or after_cursor):
                response = requests.get(url, headers=headers, params=query_parameters)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data and json_data.get('data', None):
                        for user_data in json_data['data']:
                            if len(users) < limit:
                                users.append(User(user_data))
                            else:
                                return users
                    after_cursor = self.get_after_cursor(response)
                    if after_cursor:
                        if not query_parameters:
                            query_parameters = {}
                        query_parameters['after_cursor'] = after_cursor
                else:
                    self.error = str(response.status_code)
                    self.error_description = self.extract_error_message_from_response(response)
                    break

            return users
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_user(self, user_id):
        """

        Gets User by ID.

        :param user_id: Id of the user
        :type user_id: int

        Returns the user identified by the id
        :return: user
        :rtype: User object

        See https://developers.onelogin.com/api-docs/1/users/get-user-by-id Get User by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_USER_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return User(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_user_apps(self, user_id):
        """

        Gets a list of apps accessible by a user, not including personal apps.

        :param user_id: Id of the user
        :type user_id: int

        Returns the apps user identified by the id
        :return: apps
        :rtype: App array

        See https://developers.onelogin.com/api-docs/1/users/get-apps-for-user Get Apps for a User documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_APPS_FOR_USER_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            apps = []
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    for app_data in json_data['data']:
                        apps.append(App(app_data))
                return apps
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_user_roles(self, user_id):
        """

        Gets a list of role IDs that have been assigned to a user.

        :param user_id: Id of the user
        :type user_id: int

        Returns the role ids of the user identified by the id
        :return: role ids
        :rtype: integer array

        See https://developers.onelogin.com/api-docs/1/users/get-roles-for-user Get Roles for a User documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_ROLES_FOR_USER_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            role_ids = []
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    role_ids = json_data['data'][0]
                return role_ids
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_custom_attributes(self):
        """

        Gets a list of all custom attribute fields (also known as custom user fields) that have been defined for OL account.

        Returns the custom attributes of the account
        :return: custom attribute list
        :rtype: string array

        See https://developers.onelogin.com/api-docs/1/users/get-custom-attributes Get Custom Attributes documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_CUSTOM_ATTRIBUTES_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            custom_attributes = []
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    custom_attributes = json_data['data'][0]
                return custom_attributes
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def create_user(self, user_params):
        """

        Creates an user

        :param user_params: User data (firstname, lastname, email, username, company,
                                       department, directory_id, distinguished_name,
                                       external_id, group_id, invalid_login_attempts,
                                       locale_code, manager_ad_id, member_of,
                                       openid_name, phone, samaccountname, title,
                                       userprincipalname)
        :type user_params: dict

        Returns the created user
        :return: user
        :rtype: User

        See https://developers.onelogin.com/api-docs/1/users/create-user Create User documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.CREATE_USER_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=user_params)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return User(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def update_user(self, user_id, user_params):
        """

        Updates an user

        :param user_id: Id of the user
        :type user_id: int

        :param user_params: User data (firstname, lastname, email, username, company,
                                       department, directory_id, distinguished_name,
                                       external_id, group_id, invalid_login_attempts,
                                       locale_code, manager_ad_id, member_of,
                                       openid_name, phone, samaccountname, title,
                                       userprincipalname)
        :type user_params: dict

        Returns the modified user
        :return: user
        :rtype: User

        See https://developers.onelogin.com/api-docs/1/users/update-user Update User by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.UPDATE_USER_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=user_params)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return User(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def assign_role_to_user(self, user_id, role_ids):
        """

        Assigns Roles to User

        :param user_id: Id of the user
        :type user_id: int

        :param role_ids: List of role ids to be added
        :type user_params: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/assign-role-to-user Assign Role to User documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.ADD_ROLE_TO_USER_URL, user_id)
            authorization = self.get_authorization()

            data = {
                'role_id_array': role_ids
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def remove_role_from_user(self, user_id, role_ids):
        """

        Remove Role from User

        :param user_id: Id of the user
        :type user_id: int

        :param role_ids: List of role ids to be removed
        :type user_params: integer array

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/remove-role-from-user Remove Role from User documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.DELETE_ROLE_TO_USER_URL, user_id)
            authorization = self.get_authorization()

            data = {
                'role_id_array': role_ids
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def set_password_using_clear_text(self, user_id, password, password_confirmation):
        """

        Sets Password by ID Using Cleartext

        :param user_id: Id of the user
        :type user_id: int

        :param password: Set to the password value using cleartext.
        :type password: string

        :param password_confirmation: Ensure that this value matches the password value exactly.
        :type password_confirmation: string

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-password-in-cleartext Set Password by ID Using Cleartext documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.SET_PW_CLEARTEXT, user_id)
            authorization = self.get_authorization()

            data = {
                'password': password,
                'password_confirmation': password_confirmation
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def set_password_using_hash_salt(self, user_id, password, password_confirmation, password_algorithm, password_salt=None):
        """

        Set Password by ID Using Salt and SHA-256

        :param user_id: Id of the user
        :type user_id: int

        :param password: Set to the password value using a SHA-256-encoded value.
        :type password: string

        :param password_confirmation: Ensure that this value matches the password value exactly.
        :type password_confirmation: string

        :param password_algorithm: Set to salt+sha256.
        :type password_algorithm: string

        :param password_salt: (Optional) To provide your own salt value.
        :type password_salt: string

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-password-using-sha-256 Set Password by ID Using Salt and SHA-256 documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.SET_PW_SALT, user_id)
            authorization = self.get_authorization()

            data = {
                'password': password,
                'password_confirmation': password_confirmation,
                'password_algorithm': password_algorithm
            }
            if password_salt:
                data["password_salt"] = password_salt

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def set_custom_attribute_to_user(self, user_id, custom_attributes):
        """

        Set Custom Attribute Value

        :param user_id: Id of the user
        :type user_id: int

        :param custom_attributes: Provide one or more key value pairs composed of the custom attribute field shortname and the value that you want to set the field to.
        :type custom_attributes: dict

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/set-custom-attribute Set Custom Attribute Value documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.SET_CUSTOM_ATTRIBUTE_TO_USER_URL, user_id)
            authorization = self.get_authorization()

            data = {
                'custom_attributes': custom_attributes
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def log_user_out(self, user_id):
        """

        Log a user out of any and all sessions.

        :param user_id: Id of the user to be logged out
        :type user_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/log-user-out Log User Out documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.LOG_USER_OUT_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def lock_user(self, user_id, minutes):
        """

        Use this call to lock a user's account based on the policy assigned to
        the user, for a specific time you define in the request, or until you
        unlock it.

        :param user_id: Id of the user to be locked.
        :type user_id: int

        :param minutes: Set to the number of minutes for which you want to lock the user account. (0 to delegate on policy)
        :type minutes: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/lock-user-account Lock User Account documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.LOCK_USER_URL, user_id)
            authorization = self.get_authorization()

            data = {
                'locked_until': minutes
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def delete_user(self, user_id):
        """

        Deletes an user

        :param user_id: Id of the user to be logged out
        :type user_id: int

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/users/delete-user Delete User by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.DELETE_USER_URL, user_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.delete(url, headers=headers)

            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Login Page Methods
    def create_session_login_token(self, query_params, allowed_origin=''):
        """

        Generates a session login token in scenarios in which MFA may or may not be required.
        A session login token expires two minutes after creation.

        :param query_params: Query Parameters (username_or_email, password, subdomain, return_to_url,
                                               ip_address, browser_id)
        :type query_params: dict

        :param allowed_origin: Custom-Allowed-Origin-Header. Required for CORS requests only.
                               Set to the Origin URI from which you are allowed to send a request
                               using CORS.
        :type allowed_origin: string

        Returns a session token
        :return: return the object if success
        :rtype: SessionTokenInfo/SessionTokenMFAInfo

        See https://developers.onelogin.com/api-docs/1/users/create-session-login-token Create Session Login Token documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.SESSION_LOGIN_TOKEN_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }
            if allowed_origin:
                headers['Custom-Allowed-Origin-Header-1'] = allowed_origin

            response = requests.post(url, headers=headers, json=query_params)

            if response.status_code == 200:
                return self.handle_session_token_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_session_token_verified(self, device_id, state_token, otp_token=None):
        """

        Verify a one-time password (OTP) value provided for multi-factor authentication (MFA).

        :param device_id: Provide the MFA device_id you are submitting for verification.
        :type device_id: string

        :param state_token: Provide the state_token associated with the MFA device_id you are submitting for verification.
        :type state_token: string

        :param otp_token: Provide the OTP value for the MFA factor you are submitting for verification.
        :type otp_token: string

        Returns a session token
        :return: return the object if success
        :rtype: SessionTokenInfo

        See https://developers.onelogin.com/api-docs/1/users/verify-factor Verify Factor documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_TOKEN_VERIFY_FACTOR)
            authorization = self.get_authorization()

            data = {
                'device_id': str(device_id),
                'state_token': state_token
            }
            if otp_token:
                data['otp_token'] = otp_token

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_session_token_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Role Methods
    def get_roles(self, query_parameters=None):
        """

        Gets a list of Role resources. (if no limit provided, by default get 50 elements)

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        Returns the list of roles
        :return: role list
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/roles/get-roles Get Roles documentation

        """
        self.clean_error()
        self.prepare_token()
        limit = 50

        if query_parameters:
            if query_parameters.get('limit', None):
                limit = int(query_parameters.get('limit'))
                if limit > 50:
                    del query_parameters['limit']

        try:
            url = self.settings.get_url(Constants.GET_ROLES_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            roles = []
            response = None
            after_cursor = None
            while (not response) or (len(roles) > limit or after_cursor):
                response = requests.get(url, headers=headers, params=query_parameters)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data and json_data.get('data', None):
                        for role_data in json_data['data']:
                            if len(roles) < limit:
                                roles.append(Role(role_data))
                            return roles

                    after_cursor = self.get_after_cursor(response)
                    if after_cursor:
                        if not query_parameters:
                            query_parameters = {}
                        query_parameters['after_cursor'] = after_cursor
                else:
                    self.error = str(response.status_code)
                    self.error_description = self.extract_error_message_from_response(response)
                    break

            return roles
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_role(self, role_id):
        """

        Gets Role by ID.

        :param role_id: Id of the Role
        :type role_id: int

        Returns the role identified by the id
        :return: role
        :rtype: Role object

        See https://developers.onelogin.com/api-docs/1/roles/get-role-by-id Get Role by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_ROLE_URL, role_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return Role(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Event Methods
    def get_event_types(self):
        """

        List of all OneLogin event types available to the Events API.

        Returns the list of event type
        :return: event type list
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/events/event-types Get Event Types documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_EVENT_TYPES_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            event_types = []
            response = None
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    for event_type_data in json_data['data']:
                        event_types.append(EventType(event_type_data))
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)

            return event_types
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_events(self, query_parameters=None):
        """

        Gets a list of Event resources. (if no limit provided, by default get 50 elements)

        :param query_parameters: Parameters to filter the result of the list
        :type query_parameters: dict

        Returns the list of events
        :return: event list
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/events/get-events Get Events documentation

        """
        self.clean_error()
        self.prepare_token()
        limit = 50

        if query_parameters:
            if query_parameters.get('limit', None):
                limit = int(query_parameters.get('limit'))
                if limit > 50:
                    del query_parameters['limit']

        try:
            url = self.settings.get_url(Constants.GET_EVENTS_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            events = []
            response = None
            after_cursor = None
            while (not response) or (len(events) > limit or after_cursor):
                response = requests.get(url, headers=headers, params=query_parameters)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data and json_data.get('data', None):
                        for event_data in json_data['data']:
                            if len(events) < limit:
                                events.append(Event(event_data))
                            else:
                                return events

                    after_cursor = self.get_after_cursor(response)
                    if after_cursor:
                        if not query_parameters:
                            query_parameters = {}
                        query_parameters['after_cursor'] = after_cursor
                else:
                    self.error = str(response.status_code)
                    self.error_description = self.extract_error_message_from_response(response)
                    break

            return events
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_event(self, event_id):
        """

        Gets Event by ID.

        :param role_id: Id of the Event
        :type role_id: int

        Returns the result of the operation
        :return: event
        :rtype: Event object

        See https://developers.onelogin.com/api-docs/1/events/get-event-by-id Get Event by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_EVENT_URL, event_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return Event(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def create_event(self, event_params):
        """

        Create an event in the OneLogin event log.

        :param event_params: Event data (event_type_id, account_id, actor_system,
                                         actor_user_id, actor_user_name, app_id,
                                         assuming_acting_user_id, custom_message,
                                         directory_sync_run_id, group_id, group_name,
                                         ipaddr, otp_device_id, otp_device_name,
                                         policy_id, policy_name, role_id, role_name,
                                         user_id, user_name)
        :type event_params: dict

        Returns if the action succeed
        :return: true if success
        :rtype: bool

        See https://developers.onelogin.com/api-docs/1/events/create-event Create Event documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.CREATE_EVENT_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=event_params)
            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Group Methods
    def get_groups(self, limit=50):
        """

        Gets a list of Group resources (element of groups limited with the limit parameter).

        :param limit: Limit the number of groups returned (optional)
        :type limit: int

        Returns the list of groups
        :return: group list
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/groups/get-groups Get Groups documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_GROUPS_URL)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            query_parameters = {}
            groups = []
            response = None
            after_cursor = None
            while (not response) or (len(groups) > limit or after_cursor):
                response = requests.get(url, headers=headers, params=query_parameters)
                if response.status_code == 200:
                    json_data = response.json()
                    if json_data and json_data.get('data', None):
                        for group_data in json_data['data']:
                            if len(groups) < limit:
                                groups.append(Group(group_data))
                            else:
                                return groups

                    after_cursor = self.get_after_cursor(response)
                    if after_cursor:
                        query_parameters['after_cursor'] = after_cursor
                else:
                    self.error = str(response.status_code)
                    self.error_description = self.extract_error_message_from_response(response)
                    break

            return groups
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_group(self, group_id):
        """

        Gets Group by ID.

        :param role_id: Id of the group
        :type role_id: int

        Returns the group identified by the id
        :return: group
        :rtype: Group object

        See https://developers.onelogin.com/api-docs/1/groups/get-group-by-id Get Group by ID documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_GROUP_URL, group_id)
            authorization = self.get_authorization()

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return Group(json_data['data'][0])
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # SAML Assertion Methods
    def get_saml_assertion(self, username_or_email, password, app_id, subdomain, ip_address=None):
        """

        Generates a SAML Assertion.

        :param username_or_email: username or email of the OneLogin user accessing the app
        :type username_or_email: string

        :param password: Password of the OneLogin user accessing the app
        :type password: string

        :param app_id: App ID of the app for which you want to generate a SAML token
        :type app_id: integer

        :param subdomain: subdomain of the OneLogin account related to the user/app
        :type subdomain: string

        :param ip_address: whitelisted IP address that needs to be bypassed (some MFA scenarios).
        :type ip_address: string

        Returns a SAMLEndpointResponse object with an encoded SAMLResponse
        :return: true if success
        :rtype: SAMLEndpointResponse

        See https://developers.onelogin.com/api-docs/1/saml-assertions/generate-saml-assertion Generate SAML Assertion documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GET_SAML_ASSERTION_URL)
            authorization = self.get_authorization()

            data = {
                'username_or_email': username_or_email,
                'password': password,
                'app_id': app_id,
                'subdomain': subdomain,
            }

            if ip_address:
                data['ip_address'] = ip_address

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_saml_endpoint_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def get_saml_assertion_verifying(self, app_id, device_id, state_token, otp_token=None, url_endpoint=None):
        """

        Verify a one-time password (OTP) value provided for a second factor when multi-factor authentication (MFA) is required for SAML authentication.

        :param app_id: App ID of the app for which you want to generate a SAML token
        :type app_id: integer

        :param devide_id: Provide the MFA device_id you are submitting for verification.
        :type subdomain: integer

        :param state_token: Provide the state_token associated with the MFA device_id you are submitting for verification.
        :type state_token: string

        :param otp_token: Provide the OTP value for the MFA factor you are submitting for verification.
        :type otp_token: string

        :param url_endpoint: Specify an url where return the response.
        :type url_endpoint: string

        Returns a SAMLEndpointResponse object with an encoded SAMLResponse
        :return: true if success
        :rtype: SAMLEndpointResponse

        See @see https://developers.onelogin.com/api-docs/1/saml-assertions/verify-factor Verify Factor documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            if url_endpoint:
                url = url_endpoint
            else:
                url = self.settings.get_url(Constants.GET_SAML_VERIFY_FACTOR)
            authorization = self.get_authorization()

            data = {
                'app_id': app_id,
                'device_id': str(device_id),
                'state_token': state_token
            }

            if otp_token:
                data['otp_token'] = otp_token

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return self.handle_saml_endpoint_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Invite Links Methods
    def generate_invite_link(self, email):
        """

        Generates an invite link for a user that you have already created in your OneLogin account.

        :param email: Set to the email address of the user that you want to generate an invite link for.
        :type email: string

        Returns the invitation link
        :return: link
        :rtype: string

        See https://developers.onelogin.com/api-docs/1/invite-links/generate-invite-link Generate Invite Link documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.GENERATE_INVITE_LINK_URL)
            authorization = self.get_authorization()

            data = {
                'email': email
            }

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                json_data = response.json()
                if json_data and json_data.get('data', None):
                    return json_data['data'][0]
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    def send_invite_link(self, email, personal_email=None):
        """

        Sends an invite link to a user that you have already created in your OneLogin account.

        :param email: Set to the email address of the user that you want to send an invite link for.
        :type email: string

        :param personal_email: If you want to send the invite email to an email other than the
                               one provided in email, provide it here. The invite link will be
                               sent to this address instead.
        :type personal_email: string

        Returns the result of the operation
        :return: True if the mail with the link was sent
        :rtype: boolean

        See https://developers.onelogin.com/api-docs/1/invite-links/send-invite-link Send Invite Link documentation

        """
        self.clean_error()
        self.prepare_token()

        try:
            url = self.settings.get_url(Constants.SEND_INVITE_LINK_URL)
            authorization = self.get_authorization()

            data = {
                'email': email
            }

            if personal_email:
                data['personal_email'] = personal_email

            headers = {
                'Authorization': authorization,
                'Content-Type': 'application/json',
                'User-Agent': self.user_agent
            }

            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return self.handle_operation_response(response)
            else:
                self.error = str(response.status_code)
                self.error_description = self.extract_error_message_from_response(response)
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]

    # Embed Apps Method
    def get_embed_apps(self, token, email):
        """

        Lists apps accessible by a OneLogin user.

        :param token: Provide your embedding token.
        :type token: string

        :param email: Provide the email of the user for which you want to return a list of embeddable apps.
        :type email: string

        Returns the embed apps
        :return: A list of Apps
        :rtype: array

        See https://developers.onelogin.com/api-docs/1/embed-apps/get-apps-to-embed-for-a-user Get Apps to Embed for a User documentation

        """
        self.clean_error()

        try:
            url = Constants.EMBED_APP_URL

            data = {
                'token': token,
                'email': email
            }

            headers = {
                'User-Agent': self.user_agent
            }

            response = requests.get(url, headers=headers, params=data)
            if response.status_code == 200 and response.content:
                return self.retrieve_apps_from_xml(response.content)
            else:
                self.error = str(response.status_code)
                if response.content:
                    self.error_description = response.content
        except Exception as e:
            self.error = 500
            self.error_description = e.args[0]
