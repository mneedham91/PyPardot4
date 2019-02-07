class LifecycleStages(object):
    """
    A class to query and use Pardot Lifecycle Stages.
    Lifecycle stages field reference: http://developer.pardot.com/kb/object-field-references#lifecycle-stage
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the lifecycle stage matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/lifecycle-stages/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['lifecycleStage'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['lifecycleStage'] = []
        elif result['total_results'] == 1:
            result['lifecycleStage'] = [result['lifecycleStage']]

        return result

    def _get(self, object_name='lifecycleStage', path=None, params=None):
        """GET requests for the Lifecycle Stage object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='lifecycleStage', path=None, params=None):
        """POST requests for the Lifecycle Stage object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
