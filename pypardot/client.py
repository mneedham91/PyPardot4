import requests
from objects.accounts import Accounts
from objects.customfields import CustomFields
from objects.customredirects import CustomRedirects
from objects.dynamiccontent import DynamicContent
from objects.emailclicks import EmailClicks
from objects.emailtemplates import EmailTemplates
from objects.forms import Forms
from objects.lifecyclehistories import LifecycleHistories
from objects.lifecyclestages import LifecycleStages
from objects.lists import Lists
from objects.listmemberships import ListMemberships
from objects.emails import Emails
from objects.prospects import Prospects
from objects.opportunities import Opportunities
from objects.prospectaccounts import ProspectAccounts
from objects.tags import Tags
from objects.tagobjects import TagObjects
from objects.users import Users
from objects.visits import Visits
from objects.visitors import Visitors
from objects.visitoractivities import VisitorActivities
from objects.campaigns import Campaigns

from errors import PardotAPIError

# Issue #1 (http://code.google.com/p/pybing/issues/detail?id=1)
# Python 2.6 has json built in, 2.5 needs simplejson
try:
    import json
except ImportError:
    import simplejson as json

BASE_URI = 'https://pi.pardot.com'


class PardotAPI(object):
    def __init__(self, email, password, user_key, version=4):
        self.email = email
        self.password = password
        self.user_key = user_key
        self.api_key = None
        self.version = version
        self.accounts = Accounts(self)
        self.campaigns = Campaigns(self)
        self.customfields = CustomFields(self)
        self.customredirects = CustomRedirects(self)
        self.dynamiccontent = DynamicContent(self)
        self.emailclicks = EmailClicks(self)
        self.emails = Emails(self)
        self.emailtemplates = EmailTemplates(self)
        self.forms = Forms(self)
        self.lifecyclehistories = LifecycleHistories(self)
        self.lifecyclestages = LifecycleStages(self)
        self.listmemberships = ListMemberships(self)
        self.lists = Lists(self)
        self.opportunities = Opportunities(self)
        self.prospects = Prospects(self)
        self.prospectaccounts = ProspectAccounts(self)
        self.tags = Tags(self)
        self.tagobjects = TagObjects(self)
        self.users = Users(self)
        self.visits = Visits(self)
        self.visitors = Visitors(self)
        self.visitoractivities = VisitorActivities(self)

    def post(self, object_name, path=None, params=None, retries=0):
        """
        Makes a POST request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        if params is None:
            params = {}
        params.update({'user_key': self.user_key, 'api_key': self.api_key, 'format': 'json'})
        try:
            self._check_auth(object_name=object_name)
            request = requests.post(self._full_path(object_name, self.version, path), data=params)
            response = self._check_response(request)
            return response
        except PardotAPIError as err:
            if err.message == 'Invalid API key or user key':
                response = self._handle_expired_api_key(err, retries, 'post', object_name, path, params)
                return response
            else:
                raise err

    def get(self, object_name, path=None, params=None, retries=0):
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
                response = self._handle_expired_api_key(err, retries, 'get', object_name, path, params)
                return response
            else:
                raise err

    def _handle_expired_api_key(self, err, retries, method, object_name, path, params):
        """
        Tries to refresh an expired API key and re-issue the HTTP request. If the refresh has already been attempted,
        an error is raised.
        """
        if retries != 0:
            raise err
        self.api_key = None
        if self.authenticate():
            response = getattr(self, method)(object_name=object_name, path=path, params=params, retries=1)
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
            auth = self.post('login', params={'email': self.email, 'password': self.password})
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
        if not self.user_key or not self.api_key:
            raise Exception('Cannot build Authorization header. user or api key is empty')
        auth_string = 'Pardot api_key=%s, user_key=%s' % (self.api_key, self.user_key)
        return {'Authorization': auth_string}
