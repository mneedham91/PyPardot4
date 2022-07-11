import requests
from .objects.accounts import Accounts
from .objects.customfields import CustomFields
from .objects.customredirects import CustomRedirects
from .objects.dynamiccontent import DynamicContent
from .objects.emailclicks import EmailClicks
from .objects.emailtemplates import EmailTemplates
from .objects.forms import Forms
from .objects.lifecyclehistories import LifecycleHistories
from .objects.lifecyclestages import LifecycleStages
from .objects.lists import Lists
from .objects.listmemberships import ListMemberships
from .objects.emails import Emails
from .objects.prospects import Prospects
from .objects.opportunities import Opportunities
from .objects.prospectaccounts import ProspectAccounts
from .objects.tags import Tags
from .objects.tagobjects import TagObjects
from .objects.users import Users
from .objects.visits import Visits
from .objects.visitors import Visitors
from .objects.visitoractivities import VisitorActivities
from .objects.campaigns import Campaigns

from .errors import PardotAPIError

# Issue #1 (http://code.google.com/p/pybing/issues/detail?id=1)
# Python 2.6 has json built in, 2.5 needs simplejson
try:
    import json
except ImportError:
    import simplejson as json

BASE_URI = 'https://pi.pardot.com'
SALESFORCE_AUTH_URL = 'https://login.salesforce.com/services/oauth2/token'


class PardotAPI(object):
    def __init__(self, email, password, client_id, client_secret, pardot_business_unit_id,version=4):
        self.email = email
        self.password = password
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

        self.client_id = client_id
        self.client_secret = client_secret
        self.pardot_business_unit_id = pardot_business_unit_id

    def get_auth_token(self):
        payload={'client_id': self.client_id,
        'client_secret': self.client_secret,
        'username': self.email,
        'password': self.password,
        'grant_type': 'password'}

        response = requests.request("POST", SALESFORCE_AUTH_URL, data=payload)
        token = response.json()['access_token']
        return token

    def request_session(self, fresh_token):

        headers = {
            "Authorization": "Bearer " + fresh_token,
            "Content-Type": "application/x-www-form-urlencoded",
            "Pardot-Business-Unit-Id":self.pardot_business_unit_id
        }
        self.session = requests.Session()
        self.session.headers = headers
        return self.session

    
    def post(self, object_name, path=None, params=None, retries=0):
        """
        Makes a POST request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        token = self.get_auth_token()
        request = self.request_session(token).post(self._full_path(object_name, self.version, path), data=params)
        response = self._check_response(request)
        return response

    def get(self, object_name, path=None, params=None, retries=0):
        """
        Makes a GET request to the API. Checks for invalid requests that raise PardotAPIErrors. If the API key is
        invalid, one re-authentication request is made, in case the key has simply expired. If no errors are raised,
        returns either the JSON response, or if no JSON was returned, returns the HTTP response status code.
        """
        token = self.get_auth_token()
        request = self.request_session(token).get(self._full_path(object_name, self.version, path), params=params)
        print('get request url : ' +self._full_path(object_name, self.version, path))
        
        response = self._check_response(request)
        return response

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