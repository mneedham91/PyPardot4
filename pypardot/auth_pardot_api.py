'''
A demonstration of how to support OAuth2
using Salesforce for authentication after 2/15/2021.

This implementation uses a subclass of the standard PardotAPI class
to demonstrate a solution without any modifications to the
original PyPardot4 code.  In this way a solution is suggested
without enforcing an architecture on the maintainers of the code.

It would be expected that this code would be retrofitted into
the codebase for later releases that support OAuth2.
'''
__author__ = 'eb'

from logging import Logger
from typing import Optional, cast

import requests

from auth_handler import AuthHandler, UserAuthHandler, OAuthHandler, TraditionalAuthHandler
from client import PardotAPI
from errors import PardotAPIError


class AuthPardotAPI(PardotAPI):

    def __init__(self, auth_handler: UserAuthHandler, version=4, logger: Optional[Logger] = None):
        super().__init__(auth_handler.username, auth_handler.password, auth_handler.get_userkey(), version)
        self.auth_handler: Optional[AuthHandler] = auth_handler
        self.logger = logger

    def use_username_authorization(self) -> bool:
        return self.auth_handler is None or isinstance(self.auth_handler, TraditionalAuthHandler)

    def authenticate(self):
        if self.use_username_authorization():
            self.logger and self.logger.debug(f"AuthPardotAPI: Authenticate Pardot with Pardot-Only user {self.email[:10]}...")
            return super().authenticate()
        else:
            oauth_handler: OAuthHandler = cast(OAuthHandler, self.auth_handler)
            self.logger and self.logger.debug(f"AuthPardotAPI: Authenticate Pardot with OAuth2 key {oauth_handler.consumer_key[:10]}...")
            success = self.auth_handler.handle_authentication()
            return success

    def post(self, object_name, path=None, params=None, retries=0):
        """
        Uses the default methodology if oauth is not required.

        Makes a POST request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        if self.use_username_authorization():
            return super().post(object_name, path=path, params=params, retries=retries)

        params = {} if params is None else params
        params.update({'format': 'json'})
        try:
            self._check_auth(object_name=object_name)
            headers = self._build_auth_header()
            request = requests.post(self._full_path(object_name, self.version, path), data=params, headers=headers)
            response = self._check_response(request)
            return response
        except PardotAPIError as err:
            if err.message == 'access_token is invalid, unknown, or malformed':
                # The handle_expired should work fine
                response = self._handle_expired_api_key(err, retries, 'post', object_name, path, params)
                return response
            else:
                raise err

    # Did not need to overload get because it uses _build_auth_header()
    # already, so proper authorization is included in the request
    # def get(self, object_name, path=None, params=None, retries=0):
    #     pass

    def _check_auth(self, object_name):
        if self.use_username_authorization():
            return super()._check_auth(object_name)

        oauth_handler: OAuthHandler = cast(OAuthHandler, self.auth_handler)
        if oauth_handler.access_token is None:
            self.authenticate()

    def _build_auth_header(self):
        if self.use_username_authorization():
            return super()._build_auth_header()

        oauth_handler: OAuthHandler = cast(OAuthHandler, self.auth_handler)
        if not oauth_handler.access_token:
            raise Exception('Cannot build Authorization header.  access_token or bus_unit_id is empty')
        return oauth_handler.auth_header()
