class Lists(object):
    """
    A class to query and use Pardot lists.
    List field reference: http://developer.pardot.com/kb/object-field-references/#list
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the lists matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-3/lists/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['list'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['list'] = []
        elif result['total_results'] == 1:
            result['list'] = [result['list']]

        return result

    def read(self, id=None):
        """
        Returns the data for the list specified by <id>.<id> is the Pardot ID of the target list.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def update(self, id=None, **kwargs):
        """
        Updates the provided data for the list specified by <id>. <id> is the Pardot ID of the list.
        """
        response = self._post(path='/do/update/id/{id}'.format(id=id), params=kwargs)
        return response

    def create(self, **kwargs):
        """
        Creates a new list using the specified data.
        """
        response = self._post(path='/do/create', params=kwargs)
        return response

    def delete(self, id=None):
        """
        Deletes the list specified by <id>. Returns HTTP 204 No Content on success.
        """
        response = self._post(path='/do/delete/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='list', path=None, params=None):
        """GET requests for the List object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='list', path=None, params=None):
        """POST requests for the List object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
