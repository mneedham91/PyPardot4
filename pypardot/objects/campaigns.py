class Campaigns(object):
    """
    A class to query and use Pardot campaigns.
    Campaign field reference: http://developer.pardot.com/kb/object-field-references/#campaign
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the campaigns matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/campaigns/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['campaign'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['campaign'] = []
        elif result['total_results'] == 1:
            result['campaign'] = [result['campaign']]

        return result

    def read(self, id=None, **kwargs):
        """
        Returns the data for the campaign specified by <id>. <id> is the Pardot ID of the target campaign."""
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response
    
    def update(self, id=None, **kwargs):
        """
        Updates the provided data for the campaign specified by <id>. <id> is the Pardot ID of the campaign."""
        response = self._post(path='/do/update/id/{id}'.format(id=id), params=kwargs)
        return response
    
    def create(self, **kwargs):
        """
        Creates a new campaign using the specified data."""
        response = self._post(path='/do/create'.format(id=id), params=kwargs)
        return response

    def _get(self, object_name='campaign', path=None, params=None):
        """GET requests for the Campaign object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='campaign', path=None, params=None):
        """POST requests for the Campaign object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
