class EmailClicks(object):
    """
    A class to query and use Pardot email clicks.
    Email clicks field reference: http://developer.pardot.com/kb/object-field-references#email-clicks
    """

    def __init__(self, client):
        self.client = client

    def query(self, search_criteria=None, result_set_criteria=None, **kwargs):
        """
        Returns the email clicks matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/batch-email-clicks/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['emailClicks'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['emailClick'] = []
        elif result['total_results'] == 1:
            result['emailClick'] = [result['emailClick']]

        return result

    def _get(self, object_name='emailClick', path=None, params=None):
        """GET requests for the email click object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='emailClick', path=None, params=None):
        """POST requests for the email click object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
