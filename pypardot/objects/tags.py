class Tags(object):
    """
    A class to query and use Pardot Tags.
    Tag field reference: http://developer.pardot.com/kb/object-field-references#tag
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the tag matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/tags/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['tag'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['tag'] = []
        elif result['total_results'] == 1:
            result['tag'] = [result['tag']]

        return result

    def read(self, id=None):
        """
        Returns the data for the tag specified by <id>. <id> is the Pardot ID of the target tag.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='tag', path=None, params=None):
        """GET requests for the Tag object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='tag', path=None, params=None):
        """POST requests for the Tag object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
