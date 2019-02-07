from ..errors import PardotAPIArgumentError


class ListMemberships(object):
    """
    A class to query and use Pardot list memberships.
    Prospect field reference: http://developer.pardot.com/kb/object-field-references#list-membership
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the list memberships matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/list-memberships/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['list_membership'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['list_membership'] = []
        elif result['total_results'] == 1:
            result['list_membership'] = [result['list_membership']]

        return result

    def create(self, list_id=None, prospect_id=None, **kwargs):
        """
        Creates a new list membership using the specified data. <list_id> is the Pardot list ID
        of the target list and <prospect_id> is the Pardot prospect ID of the target prospect.
        Opting out prospect from list may also be added with this request.
        """
        if not list_id:
            raise PardotAPIArgumentError('a list ID is required to create a list membership.')
        if not prospect_id:
            raise PardotAPIArgumentError('a prospect ID is required to create a list membership.')
        response = self._post(path='/do/create/list_id/{list_id}/prospect_id/{prospect_id}'.format(list_id=list_id,prospect_id=prospect_id), params=kwargs)
        return response

    def read(self, list_id=None, prospect_id=None, **kwargs):
        """
        Returns the data for the list membership specified by <list_id> and <prospect_id>.
        <list_id> is the Pardot list ID of the list and <prospect_id> is the Pardot prospect ID
        of the prospect for the target list membership.
        """
        if not list_id:
            raise PardotAPIArgumentError('a list id is required to read a list membership.')
        if not prospect_id:
            raise PardotAPIArgumentError('a prospect id is required to read a list membership.')
        response = self._post(path='/do/read/list_id/{list_id}/prospect_id/{prospect_id}'.format(list_id=list_id,prospect_id=prospect_id), params=kwargs)
        return response

    def read_by_id(self, id=None, **kwargs):
        """
        Returns the data for the list membership specified by <id>. <id> is the Pardot ID of the target list membership.
        """
        if not id:
            raise PardotAPIArgumentError('ID is required to read a list membership.')
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def update(self, list_id=None, prospect_id=None, **kwargs):
        """
        Updates the provided data for a list membership specified by <list_id> and <prospect_id>.
        <list_id> is the Pardot list ID of the list and <prospect_id> is the Pardot prospect ID
        of the prospect for the target list membership. Fields that are not updated by the request remain unchanged.
        """
        if not list_id:
            raise PardotAPIArgumentError('a list ID is required to update a list membership.')
        if not prospect_id:
            raise PardotAPIArgumentError('a prospect ID is required to update a list membership.')
        response = self._post(path='/do/update/list_id/{list_id}/prospect_id/{prospect_id}'.format(list_id=list_id,prospect_id=prospect_id), params=kwargs)
        return response

    def update_by_id(self, id=None, **kwargs):
        """
        Updates the provided data for a list membership specified by <id>. <id> is the Pardot ID of the target list membership.
        Fields that are not updated by the request remain unchanged.
        """
        if not id:
            raise PardotAPIArgumentError('id is required to update a list membership.')
        response = self._post(path='/do/update/id/{id}'.format(id=id), params=kwargs)
        return response

    def delete(self, list_id=None, prospect_id=None, **kwargs):
        """
        Deletes the list membership specified by <list_id> and <prospect_id>.
        <list_id> is the Pardot list ID of the list and <prospect_id> is the Pardot prospect ID
        of the prospect for the target list membership. Returns HTTP 204 No Content on success.
        """
        if not list_id:
            raise PardotAPIArgumentError('a list ID is required to delete a list membership.')
        if not prospect_id:
            raise PardotAPIArgumentError('a prospect ID is required to delete a list membership.')
        response = self._post(path='/do/delete/list_id/{list_id}/prospect_id/{prospect_id}'.format(list_id=list_id,prospect_id=prospect_id), params=kwargs)
        if response == 204:
            return True
        return False

    def delete_by_id(self, id=None, **kwargs):
        """
        Deletes the list membership specified by <id>. <id> is the Pardot ID of the target list membership.
        Returns HTTP 204 No Content on success.
        """
        if not id:
            raise PardotAPIArgumentError('id is required to delete a list membership.')
        response = self._post(path='/do/delete/id/{id}'.format(id=id), params=kwargs)
        if response == 204:
            return True
        return False

    def _get(self, object_name='listMembership', path=None, params=None):
        """GET requests for the List Membership object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='listMembership', path=None, params=None):
        """POST requests for the List Membership object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
