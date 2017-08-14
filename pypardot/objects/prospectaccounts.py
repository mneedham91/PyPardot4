class ProspectAccounts(object):
    """
    A class to query and use Pardot prospect accounts.
    Prospect account field reference: http://developer.pardot.com/kb/object-field-references/#prospect-account
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the prospect accounts matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/prospect-accounts/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['prospectAccount'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['prospectAccount'] = []
        elif result['total_results'] == 1:
            result['prospectAccount'] = [result['prospectAccount']]

        return result

    def create(self, **kwargs):
        """Creates a new prospect account."""
        response = self._post(path='/do/create', params=kwargs)
        return response

    def describe(self, **kwargs):
        """
        Returns the field metadata for prospect accounts, explaining what fields are available, their types, whether
        they are required, and their options (for dropdowns, radio buttons, etc).
        """
        response = self._get(path='/do/describe', params=kwargs)
        return response

    def read(self, id=None, **kwargs):
        """
        Returns the data for the prospect account specified by <id>. <id> is the Pardot ID of the target prospect
        account.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def update(self, id=None, **kwargs):
        """
        Updates the data for the prospect account specified by <id>. <id> is the Pardot ID of the target prospect
        account.
        """
        response = self._post(path='/do/update/id/{id}'.format(id=id), params=kwargs)
        return response
    
    def assign(self, id=None, user_id=None, **kwargs):
        """
        Assigns the prospect account to a user specified by <user_id>. <id> is the Pardot ID of the target prospect account.
        """
        response = self._post(path='/do/assign/id/{id}'.format(id=id), params=kwargs)
        return response

    def _get(self, object_name='prospectAccount', path=None, params=None):
        """GET requests for the Prospect Account object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='prospectAccount', path=None, params=None):
        """POST requests for the Prospect Account object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
