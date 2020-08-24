class Users(object):
    """
    A class to query and use Pardot users.
    User field reference: http://developer.pardot.com/kb/api-version-3/object-field-references/#user
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the users matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-3/users/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['users'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['user'] = []
        elif result['total_results'] == 1:
            result['user'] = [result['user']]

        return result

    def read_by_id(self, id=None, **kwargs):
        """
        Returns the data for the user specified by <id>. <id> is the Pardot ID of the target user."""
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def read_by_email(self, email=None, **kwargs):
        """
        Returns the data for the user specified by <email>. <email> is the email address of the target user."""
        response = self._post(path='/do/read/email/{email}'.format(email=email), params=kwargs)
        return response

    def _get(self, object_name='user', path=None, params=None):
        """GET requests for the User object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='user', path=None, params=None):
        """POST requests for the User object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
