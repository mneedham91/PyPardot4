import logging
import requests
import sys
from urllib.parse import parse_qs, urlparse

from .errors import PardotAPIError

# Issue #1 (http://code.google.com/p/pybing/issues/detail?id=1)
# Python 2.6 has json built in, 2.5 needs simplejson
try:
    import json
except ImportError:
    import simplejson as json

BASE_URI = 'https://pi.pardot.com'

logger = logging.getLogger(__name__)


class PardotAPI(object):
    def __init__(self, email=None, password=None, user_key=None,
                 sf_consumer_key=None, sf_consumer_secret=None,
                 sf_refresh_token=None, business_unit_id=None,
                 version=4):
        self.email = email
        self.password = password
        self.user_key = user_key
        self.api_key = None
        self.version = version
        self.sftoken = "dummy"  # trigger refresh token
        self.sftoken_refresh = sf_refresh_token
        self.sf_consumer_key = sf_consumer_key
        self.sf_consumer_secret = sf_consumer_secret
        self.business_unit_id = business_unit_id
        self._load_objects()

    def _load_objects(self):
        if self.version == 3:
            from .objects_v3 import load_objects
        else:
            from .objects import load_objects
        load_objects(self)

    def setup_salesforce_auth_keys(self, instance_id=None, business_unit_id=None, consumer_key=None, consumer_secret=None):
        print("""If you have not created Connected App, do the following:
    1. Login to Salesforce. Switch to Lightening Experience if on classic (right-top link).
    2. Cog->Setup (right top)
    3. Type 'app manager' and select App Manager from the Quick Find on the left pane
       (If you cannot see App Manager, follow this: https://help.salesforce.com/articleView?id=000322274&type=1&mode=1 )
    5. Click on the New Connected App (in the upper right corner).
    6. On the New Connected App page, fill the following required fields under Basic Information: Connected App Name, API Name and Contact Email.
    7. Go to API (Enable OAuth Settings), and select Enable OAuth Settings. In the Callback URL field, enter https://login.salesforce.com/. In the Selected OAuth Scopes field, select Access and manage your data (api), Perform requests on your behalf at any time (refresh_token, offline_access), Provide access to your data via the Web (web), Access Pardot services (pardot_api), and then click Add.
    8. Click the Save button to save the new Connected App.
    Credit: Instruction adopted from https://medium.com/@bpmmendis94/obtain-access-refresh-tokens-from-salesforce-rest-api-a324fe4ccd9b#:~:text=In%20the%20left%2Dhand%20pane,and%20select%20Enable%20OAuth%20Settings""")
        if not instance_id:
            print("""Get your instance ID:
Login to Salesforce and grab the first part of URL (ex. na112 for https://na112.lightning.force.com/)""")
            sys.stdout.write("What is your instance ID?: ")
            instance_id = input()
        if not business_unit_id:
            print("""Get your Pardot business unit ID
To find the Pardot Business Unit ID, use Setup in Salesforce. From Setup, enter "Pardot Account Setup" in the Quick Find box. Your Pardot Business Unit ID begins with "0Uv" and is 18 characters long. If you cannot access the Pardot Account Setup information, ask your Salesforce Administrator to provide you with the Pardot Business Unit ID.
(From https://developer.pardot.com/kb/authentication/ )""")
            sys.stdout.write("What is your business unit ID?: ")
            self.business_unit_id = input()
        if not consumer_key or not consumer_secret:
            print("""Get your consumer key:
    1. Login to Salesforce. Switch to Lightening Experience if on classic (right-top link).
    2. Cog->Setup (right top)
    3. Type 'app manager' and select App Manager from the Quick Find on the left pane
    4. Find the target Connected App and click on the down arrow and select view.""")
            sys.stdout.write("What is your consumer key?: ")
            self.sf_consumer_key = input()
            sys.stdout.write("What is your consumer secret?: ")
            self.sf_consumer_secret = input()
        url = f"https://{instance_id}.salesforce.com/services/oauth2/authorize?response_type=code&client_id={self.sf_consumer_key}&redirect_uri=https://login.salesforce.com/"
        print(f"""\nOpen the following page in a browser {url}.
Allow access if any alert popup. You will be redirected to a login page, but do not login.""")
        sys.stdout.write("Copy and page the entire URL of the login page that contains code: ")
        new_url = input()
        parsed = urlparse(new_url)
        code = parse_qs(parsed.query)["code"][0]

        post_url = f"https://login.salesforce.com/services/oauth2/token?code={code}&grant_type=authorization_code&client_id={self.sf_consumer_key}&client_secret={self.sf_consumer_secret}&redirect_uri=https://login.salesforce.com/"
        response = requests.post(post_url).json()
        self.sftoken = response.get("access_token")
        self.sftoken_refresh = response.get("refresh_token")
        if not self.sftoken:
            raise Exception("Failed to obtain token %s" % response)

    def revoke_sf_token(self):
        url = "https://login.salesforce.com/services/oauth2/revoke"
        # header = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url,
                                 data={"token": self.sftoken})
        if response.status_code >= 400:
            raise Exception(response)

    def refresh_sf_token(self):
        url = "https://login.salesforce.com/services/oauth2/token"
        data = {"grant_type": "refresh_token",
                "client_id": self.sf_consumer_key,
                "client_secret": self.sf_consumer_secret,
                "refresh_token": self.sftoken_refresh}
        response = requests.post(url, data=data).json()
        self.sftoken = response.get("access_token")
        if not self.sftoken:
            raise Exception(f"Failed to refresh token: {response}")

    def post(self, object_name, path=None,
              headers=None, params=None, data=None, json=None, files=None,
              retries=0):
        """
        Makes a POST request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        if headers is None:
            headers = {}
        if self.api_key or self.sftoken:
            auth_headers = self._build_auth_header()
            headers.update(auth_headers)

        if params is None:
            params = {}
        params.update({'format': 'json'})

        if data is None and json is None:
            data = {}
        if data is not None:
            if 'password' in data.keys():
                data.update({'user_key': self.user_key, 'api_key': self.api_key})

        if files:
            for _, f in files.items():
                f.seek(0)

        try:
            self._check_auth(object_name=object_name)
            request = requests.post(self._full_path(object_name, self.version, path),
                                    headers=headers,
                                    params=params,
                                    data=data,
                                    files=files,
                                    json=json)

            # some endpoints (import/add_batch) returns an empty response
            if request.content:
                response = self._check_response(request)
                return response
            return None
        except PardotAPIError as err:
            if err.message == 'Invalid API key or user key':
                response = self._handle_expired_api_key(
                    err, retries, 'post', headers, object_name, path, params, data, files)
                return response
            elif err.message == 'access_token is invalid, unknown, or malformed':
                response = self._handle_expired_token(
                    err, retries, 'post', headers, object_name, path, params, data, files)
                return response
            else:
                raise err

    def patch(self, object_name, path=None,
              headers=None, params=None, data=None, json=None, files=None,
              retries=0):
        """
        Makes a PATCH request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        if headers is None:
            headers = {}

        if self.api_key or self.sftoken:
            auth_headers = self._build_auth_header()
            headers.update(auth_headers)

        if params is None:
            params = {}
        params.update({'format': 'json'})

        if data is None and json is None:
            data = {}
        if data is not None:
            if 'password' in data.keys():
                data.update({'user_key': self.user_key, 'api_key': self.api_key})

        try:
            self._check_auth(object_name=object_name)
            request = requests.patch(self._full_path(object_name, self.version, path),
                                     headers=headers,
                                     params=params,
                                     data=data,
                                     json=json,
                                     files=files)

            if request.content:
                response = self._check_response(request)
                return response
            return None
        except PardotAPIError as err:
            if err.message == 'Invalid API key or user key':
                response = self._handle_expired_api_key(
                    err, retries, 'patch', headers, object_name, path, params, data, files)
                return response
            elif err.message == 'access_token is invalid, unknown, or malformed':
                response = self._handle_expired_token(
                    err, retries, 'patch', headers, object_name, path, params, data, files)
                return response
            else:
                raise err


    def get(self, object_name, path=None, params=None, retries=0, **kwargs):
        """
        Makes a GET request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        if params is None:
            params = {}
        params.update({'format': 'json'})
        headers = self._build_auth_header()
        try:
            self._check_auth(object_name=object_name)
            request = requests.get(self._full_path(object_name, self.version, path), params=params, headers=headers)
            response = self._check_response(request)
            return response
        except PardotAPIError as err:
            if err.message == 'Invalid API key or user key':
                response = self._handle_expired_api_key(
                    err, retries, 'get', headers, object_name, path, params)
                return response
            elif err.message == 'access_token is invalid, unknown, or malformed':
                response = self._handle_expired_token(
                    err, retries, 'get', headers, object_name, path, params)
                return response
            else:
                raise err

    def _handle_expired_api_key(self, err, retries, method, headers, object_name, path, params, data=None, files=None):
        """
        Tries to refresh an expired API key and re-issue the HTTP request. If the refresh has already been attempted,
        an error is raised.
        """
        if retries != 0:
            raise err
        self.api_key = None
        if self.authenticate():
            response = getattr(self, method)(
                object_name=object_name, path=path, params=params, data=data,
                files=files, headers=headers, retries=1)
            return response
        else:
            raise err

    def _handle_expired_token(self, err, retries, method, headers, object_name, path, params, data=None, files=None):
        """
        Tries to refresh an expired token and re-issue the HTTP request. If the refresh has already been attempted,
        an error is raised.
        """
        if retries != 0:
            raise err
        self.sftoken = None
        self.refresh_sf_token()
        if self.sftoken:
            response = getattr(self, method)(
                object_name=object_name, path=path, params=params, data=data,
                files=files, headers=headers, retries=1)
            return response
        else:
            raise err

    @staticmethod
    def _full_path(object_name, version, path=None):
        """Builds the full path for the API request"""
        full = '{0}/api/{1}/version/{2}'.format(BASE_URI, object_name, version)
        if path:
            return full + '{0}'.format(path)
        return full

    @staticmethod
    def _check_response(response):
        """
        Checks the HTTP response to see if it contains JSON. If it does, checks the JSON for error codes and messages.
        Raises PardotAPIError if an error was found. If no error was found, returns the JSON. If JSON was not found,
        returns the response status code.
        """
        if response.headers.get('content-type') == 'application/json':
            json = response.json()
            error = json.get('err')
            if error:
                raise PardotAPIError(json_response=json)
            return json
        else:
            return response.status_code

    def _check_auth(self, object_name):
        if object_name == 'login':
            return
        if self.api_key is None:
            self.authenticate()

    def authenticate(self):
        """
         Authenticates the user and sets the API key if successful. Returns True if authentication is successful,
         False if authentication fails.
        """
        try:
            auth = self.post('login', data={'email': self.email, 'password': self.password})
            if type(auth) is int:
                # sometimes the self.post method will return a status code instead of JSON response on failures
                return False
            self.api_key = auth.get('api_key', None)
            if self.api_key is not None:
                return True
            return False
        except PardotAPIError:
            return False

    def _build_auth_header(self):
        """
        Builds Pardot Authorization Header to be used with GET requests
        """
        if self.sftoken and self.business_unit_id:
            return {"Authorization": "Bearer " + self.sftoken, "Pardot-Business-Unit-Id": self.business_unit_id}
        if not self.user_key or not self.api_key:
            raise Exception('Cannot build Authorization header. user or api key is empty')
        auth_string = 'Pardot api_key=%s, user_key=%s' % (self.api_key, self.user_key)
        return {'Authorization': auth_string}
