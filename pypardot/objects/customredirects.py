class CustomRedirects(object):
    """
    A class to query and use Pardot Custom Redirects.
    Custom redirects field reference: http://developer.pardot.com/kb/object-field-references#custom-redirect
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the custom redirects matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/custom-redirects/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['customRedirect'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['customRedirect'] = []
        elif result['total_results'] == 1:
            result['customRedirect'] = [result['customRedirect']]

        return result

    def read(self, id=None):
        """
        Returns the data for the custom redirect specified by <id>. <id> is the Pardot ID of the target custom redirect.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='customRedirect', path=None, params=None):
        """GET requests for the Custom Redirect object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='customRedirect', path=None, params=None):
        """POST requests for the Custom Redirect object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
