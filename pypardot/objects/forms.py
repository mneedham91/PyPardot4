class Forms(object):
    """
    A class to query and use Pardot Forms.
    Forms field reference: http://developer.pardot.com/kb/object-field-references#form
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the forms matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/forms/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['form'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['form'] = []
        elif result['total_results'] == 1:
            result['form'] = [result['form']]

        return result

    def read(self, id=None):
        """
        Returns the data for the form specified by <id>. <id> is the Pardot ID of the target list.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='form', path=None, params=None):
        """GET requests for the Form object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='form', path=None, params=None):
        """POST requests for the Form object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
