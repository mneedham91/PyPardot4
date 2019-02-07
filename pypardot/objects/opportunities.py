class Opportunities(object):
    """
    A class to query and use Pardot opportunities.
    Opportunity field reference: http://developer.pardot.com/kb/object-field-references#opportunity
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the opportunities matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/opportunities/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['opportunity'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['opportunity'] = []
        elif result['total_results'] == 1:
            result['opportunity'] = [result['opportunity']]

        return result

    def create_by_email(self, prospect_email=None, name=None, value=None, probability=None, **kwargs):
        """
        Creates a new opportunity using the specified data. <prospect_email> must correspond to an existing prospect.
        """
        kwargs.update({'name': name, 'value': value, 'probability': probability})
        response = self._post(
            path='/do/create/prospect_email/{prospect_email}'.format(prospect_email=prospect_email),
            params=kwargs)
        return response

    def create_by_id(self, prospect_id=None, name=None, value=None, probability=None, **kwargs):
        """
        Creates a new opportunity using the specified data. <prospect_id> must correspond to an existing prospect.
        """
        kwargs.update({'name': name, 'value': value, 'probability': probability})
        response = self._post(
            path='/do/create/prospect_id/{prospect_id}'.format(prospect_id=prospect_id),
            params=kwargs)
        return response

    def read(self, id=None):
        """
        Returns the data for the opportunity specified by <id>, including campaign assignment and associated visitor
        activities. <id> is the Pardot ID for the target opportunity.
        """
        response = self._post(path='/do/read/id/{id}'.format(id=id))
        return response

    def update(self, id=None):
        """
        Updates the provided data for the opportunity specified by <id>. <id> is the Pardot ID for the target
        opportunity. Fields that are not updated by the request remain unchanged. Returns an updated version of the
        opportunity.
        """
        response = self._post(path='/do/update/id/{id}'.format(id=id))
        return response

    def delete(self, id=None):
        """
        Deletes the opportunity specified by <id>. <id> is the Pardot ID for the target opportunity. Returns no response
        on success.
        """
        response = self._post(path='/do/delete/id/{id}'.format(id=id))
        return response

    def undelete(self, id=None):
        """
        Un-deletes the opportunity specified by <id>. <id> is the Pardot ID for the target opportunity. Returns no
        response on success.
        """
        response = self._post(path='/do/undelete/id/{id}'.format(id=id))
        return response

    def _get(self, object_name='opportunity', path=None, params=None):
        """GET requests for the Opportunity object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='opportunity', path=None, params=None):
        """POST requests for the Opportunity object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
