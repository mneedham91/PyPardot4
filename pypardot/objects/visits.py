class Visits(object):
    """
    A class to query and use Pardot visits.
    Visit field reference: http://developer.pardot.com/kb/object-field-references/#visit
    """

    def __init__(self, client):
        self.client = client

    def query_by_ids(self, ids=None, **kwargs):
        """Returns the visits matching the given <ids>. The <ids> should be comma separated integers (no spaces)."""
        kwargs['ids'] = ids.replace(' ', '')
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['visit'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['visit'] = []
        elif result['total_results'] == 1:
            result['visit'] = [result['visit']]

        return result

    def query_by_visitor_ids(self, visitor_ids=None, **kwargs):
        """
        Returns the visits matching the given <visitor ids>. The <visitor ids> should be comma separated integers
        (no spaces).
        """
        kwargs['visitor_ids'] = visitor_ids.replace(' ', '')
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['visit'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['visit'] = []
        elif result['total_results'] == 1:
            result['visit'] = [result['visit']]

        return result

    def query_by_prospect_ids(self, prospect_ids=None, **kwargs):
        """
        Returns the visits matching the given <prospect ids>. The <prospect ids> should be comma separated integers
        (no spaces).
        """
        kwargs['prospect_ids'] = prospect_ids.replace(' ', '')
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['visit'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['visit'] = []
        elif result['total_results'] == 1:
            result['visit'] = [result['visit']]

        return result

    def read(self, id=None, **kwargs):
        """
        Returns the data for the visit specified by <id>. <id> is the Pardot ID of the target visit."""
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def _get(self, object_name='visit', path=None, params=None):
        """GET requests for the Visit object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='visit', path=None, params=None):
        """POST requests for the Visit object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
