class Accounts(object):
    """
    A class to query and use Pardot  accounts.
    Account field reference: http://developer.pardot.com/kb/object-field-references/#account
    """

    def __init__(self, client):
        self.client = client

    def read(self, **kwargs):
        """
        Returns the data for the account of the currently logged in user.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def _get(self, object_name='account', path=None, params=None):
        """GET requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='account', path=None, params=None):
        """POST requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
