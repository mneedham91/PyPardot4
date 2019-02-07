class CustomFields(object):
    """
    A class to query and use Pardot Custom Fields.
    Custom fields field reference: http://developer.pardot.com/kb/object-field-references
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the custom fields matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/custom-fields/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['customField'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['customField'] = []
        elif result['total_results'] == 1:
            result['customField'] = [result['customField']]

        return result

    def create(self, **kwargs):
        """
        Creates a new custom field using the specified data.
        """
        response = self._post(path='/do/create', params=kwargs)
        return response

    def read(self, id=None):
        """
        Returns the data for the custom field specified by <id>. <id> is the Pardot ID of the target custom field.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def update(self, id=None, **kwargs):
        """
        Updates the provided data for the custom field specified by <id>. <id> is the Pardot ID of the custom field.
        Refer to Custom Field in Object Field References for more details. Returns the updated version of the custom field.
        """
        response = self._post(path='/do/update/id/{id}'.format(id=id))
        return response

    def delete(self, id=None):
        """
        Deletes the custom field specified by <id>. Returns HTTP 204 No Content on success.
        """
        response = self._post(path='/do/delete/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='customField', path=None, params=None):
        """GET requests for the Custom Field object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='customField', path=None, params=None):
        """POST requests for the Custom Field object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
