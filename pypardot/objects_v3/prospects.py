from ..errors import PardotAPIArgumentError


class Prospects(object):
    """
    A class to query and use Pardot prospects.
    Prospect field reference: http://developer.pardot.com/kb/api-version-3/object-field-references/#prospect
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the prospects matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-3/prospects/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['prospect'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['prospect'] = []
        elif result['total_results'] == 1:
            result['prospect'] = [result['prospect']]

        return result

    def assign_by_email(self, email=None, **kwargs):
        """
        Assigns or reassigns the prospect specified by <email> to a specified Pardot user or group. One (and only one)
        of the following parameters must be provided to identify the target user or group: <user_email>, <user_id>, or
        <group_id>. Returns an updated version of the prospect.
        """
        response = self._post(path='/do/assign/email/{email}'.format(email=email), params=kwargs)
        return response

    def assign_by_id(self, id=None, **kwargs):
        """
        Assigns or reassigns the prospect specified by <id> to a specified Pardot user or group. One (and only one) of
        the following parameters must be provided to identify the target user or group: <user_email>, <user_id>, or
        <group_id>. Returns an updated version of the prospect.
        """
        response = self._post(path='/do/assign/id/{id}'.format(id=id), params=kwargs)
        return response

    def unassign_by_email(self, email=None, **kwargs):
        """Unassigns the prospect specified by <email>. Returns an updated version of the prospect."""
        response = self._post(path='/do/unassign/email/{email}'.format(email=email), params=kwargs)
        return response

    def unassign_by_id(self, id=None, **kwargs):
        """Unassigns the prospect specified by <id>. Returns an updated version of the prospect."""
        response = self._post(path='/do/unassign/id/{id}'.format(id=id), params=kwargs)
        return response

    def create_by_email(self, email=None, **kwargs):
        """
        Creates a new prospect using the specified data. <email> must be a unique email address. Returns the new prospect.
        """
        if not email:
            raise PardotAPIArgumentError('email is required to create a prospect.')
        response = self._post(path='/do/create/email/{email}'.format(email=email), params=kwargs)
        return response

    def read_by_email(self, email=None, **kwargs):
        """
        Returns data for the prospect specified by <email>, including campaign assignment, profile criteria
        matching statuses, associated visitor activities, email list subscriptions, and custom field data.
        <email> is the email address of the target prospect.
        """
        if not email:
            raise PardotAPIArgumentError('email is required to read a prospect.')
        response = self._post(path='/do/read/email/{email}'.format(email=email), params=kwargs)
        return response

    def read_by_id(self, id=None, **kwargs):
        """
        Returns data for the prospect specified by <id>, including campaign assignment, profile criteria
        matching statuses, associated visitor activities, email list subscriptions, and custom field data.
        <id> is the Pardot ID of the target prospect.
        """
        if not id:
            raise PardotAPIArgumentError('id is required to read a prospect.')
        response = self._post(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def update_by_email(self, email=None, **kwargs):
        """
        Updates the provided data for a prospect specified by <email>. <email> is the email address of the
        prospect. Fields that are not updated by the request remain unchanged.
        """
        if not email:
            raise PardotAPIArgumentError('email is required to update a prospect.')
        response = self._post(path='/do/update/email/{email}'.format(email=email), params=kwargs)
        return response

    def update_by_id(self, id=None, **kwargs):
        """
        Updates the provided data for a prospect specified by <id>. <id> is the Pardot ID of the prospect.
        Fields that are not updated by the request remain unchanged.
        """
        if not id:
            raise PardotAPIArgumentError('id is required to update a prospect.')
        response = self._post(path='/do/update/id/{id}'.format(id=id), params=kwargs)
        return response

    def upsert_by_email(self, email=None, **kwargs):
        """
        Updates the provided data for the prospect specified by <email>. If a prospect with the provided email address
        does not yet exist, a new prospect is created using the <email> value. Fields that are not updated by the
        request remain unchanged.
        """
        if not email:
            raise PardotAPIArgumentError('email is required to upsert a prospect.')
        response = self._post(path='/do/upsert/email/{email}'.format(email=email), params=kwargs)
        return response

    def upsert_by_id(self, id=None, **kwargs):
        """
        Updates the provided data for the prospect specified by <id>. If an <email> value is provided, it is used to
        update the prospect's email address. If a prospect with the provided ID is not found, Pardot searches for a
        prospect identified by <email>. If a prospect with the provided email address does not yet exist, a new
        prospect is created using <email> value. Fields that are not updated by the request remain unchanged.
        """
        if not id:
            raise PardotAPIArgumentError('id is required to upsert a prospect.')
        response = self._post(path='/do/upsert/id/{id}'.format(id=id), params=kwargs)
        return response

    def delete_by_email(self, email=None, **kwargs):
        """Deletes the prospect specified by <email>. Returns True if operation was successful."""
        if not email:
            raise PardotAPIArgumentError('email is required to delete a prospect.')
        response = self._post(path='/do/delete/email/{email}'.format(email=email), params=kwargs)
        if response == 204:
            return True
        return False

    def delete_by_id(self, id=None, **kwargs):
        """Deletes the prospect specified by <id>. Returns True if operation was successful."""
        if not id:
            raise PardotAPIArgumentError('id is required to delete a prospect.')
        response = self._post(path='/do/delete/id/{id}'.format(id=id), params=kwargs)
        if response == 204:
            return True
        return False

    def update_field_by_id(self, id=None, field_name=None, field_value=None):
        """Updates the provided field for the prospect specified by <id>. Returns the updated prospect."""
        response = self.update_by_id(id=id, **{field_name: field_value})
        return response

    def update_field_by_email(self, email=None, field_name=None, field_value=None):
        """Updates the provided field for the prospect specified by <email>. Returns the updated prospect."""
        response = self.update_by_email(email=email, **{field_name: field_value})
        return response

    def read_field_by_email(self, email=None, field_name=None):
        """Returns the value of the provided field for the prospect specified by <email>."""
        response = self.read_by_email(email=email)
        return response.get('prospect').get(field_name)

    def read_field_by_id(self, id=None, field_name=None):
        """Returns the value of the provided field for the prospect specified by <id>."""
        response = self.read_by_id(id=id)
        return response.get('prospect').get(field_name)

    def add_to_list(self, prospect_id=None, list_id=None):
        """Adds the prospect specified by <prospect_id> to the list specified by <list_id>."""
        params = {'prospect_id': prospect_id, 'list_id': list_id}
        response = self._post(object_name='listMembership', path='/do/create', params=params)
        return response

    def _get(self, object_name='prospect', path=None, params=None):
        """GET requests for the Prospect object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='prospect', path=None, params=None):
        """POST requests for the Prospect object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
