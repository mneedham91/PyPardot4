class LifecycleHistories(object):
    """
    A class to query and use Pardot Lifecycle Histories.
    Lifecycle histories field reference: http://developer.pardot.com/kb/object-field-references#lifecycle-history
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the lifecycle history matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/lifecycle-histories/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['lifecycleHistory'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['lifecycleHistory'] = []
        elif result['total_results'] == 1:
            result['lifecycleHistory'] = [result['lifecycleHistory']]

        return result

    def read(self, id=None):
        """
        Returns the data for the lifecycle history specified by <id>. <id> is the Pardot ID of the target lifecycle history.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='lifecycleHistory', path=None, params=None):
        """GET requests for the Lifecycle History object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='lifecycleHistory', path=None, params=None):
        """POST requests for the Lifecycle History object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
