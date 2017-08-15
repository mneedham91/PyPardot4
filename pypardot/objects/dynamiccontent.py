class DynamicContent(object):
    """
    A class to query and use Pardot dynamic content.
    Dynamic content field reference: http://developer.pardot.com/kb/object-field-references#dynamic-content
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the dynamic content matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/dynamic-content/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['dynamicContent'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['dynamicContent'] = []
        elif result['total_results'] == 1:
            result['dynamicContent'] = [result['dynamicContent']]

        return result
    
    def read(self, id=None):
        """
        Returns the data for the dynamic content specified by <id>. <id> is the Pardot ID of the target dynamic content.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='dynamicContent', path=None, params=None):
        """GET requests for the dynamic content object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='dynamicContent', path=None, params=None):
        """POST requests for the dynamic content object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
