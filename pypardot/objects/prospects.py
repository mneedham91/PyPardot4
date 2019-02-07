from ..errors import PardotAPIArgumentError


class Prospects(object):
    """
    A class to query and use Pardot prospects.
    Prospect field reference: http://developer.pardot.com/kb/object-field-references#prospect
    """

    def __init__(self, client):
        self.client = client

    def query(self, **kwargs):
        """
        Returns the prospects matching the specified criteria parameters.
        Supported search criteria: http://developer.pardot.com/kb/api-version-4/prospects/#supported-search-criteria
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['prospect'] is a list, no matter what.
        result = response.get('result')
        if 'output' not in kwargs.keys() and 'bulk' not in kwargs.values():
            if result['total_results'] == 0:
                result['prospect'] = []
            elif result['total_results'] == 1:
                result['prospect'] = [result['prospect']]

        return result

    def assign_by_fid(self, fid=None, **kwargs):
        """
        Assigns or reassigns the prospect specified by <fid> to a specified Pardot user or group. <fid> must be a valid CRM FID.
        One (and only one) of the following parameters must be provided to identify the target user or group: <user_email>, <user_id>, or <group_id>.
        Returns an updated version of the prospect.
        """
        response = self._post(path='/do/assign/fid/{fid}'.format(fid=fid), params=kwargs)
        return response

    def assign_by_id(self, id=None, **kwargs):
        """
        Assigns or reassigns the prospect specified by <id> to a specified Pardot user or group. One (and only one) of
        the following parameters must be provided to identify the target user or group: <user_email>, <user_id>, or
        <group_id>. Returns an updated version of the prospect.
        """
        response = self._post(path='/do/assign/id/{id}'.format(id=id), params=kwargs)
        return response

    def unassign_by_fid(self, fid=None, **kwargs):
        """Unassigns the prospect specified by <fid>. Returns an updated version of the prospect."""
        response = self._post(path='/do/unassign/fid/{fid}'.format(fid=fid), params=kwargs)
        return response

    def unassign_by_id(self, id=None, **kwargs):
        """Unassigns the prospect specified by <id>. Returns an updated version of the prospect."""
        response = self._post(path='/do/unassign/id/{id}'.format(id=id), params=kwargs)
        return response

    def create(self, email=None, **kwargs):
        """
        Creates a new prospect using the specified data. <email> must be a unique email address.
        May optionally include a crm fid <fid>. Returns the new prospect.
        """
        if not email:
            raise PardotAPIArgumentError('email is required to create a prospect.')
        response = self._post(path='/do/create/email/{email}'.format(email=email), params=kwargs)
        return response

    def batchCreate(self, **kwargs):
        """
        Creates new prospects using the provided <data> in either XML or JSON.
        See Endpoints for Batch Processing: http://developer.pardot.com/kb/api-version-4/prospects/#endpoints-for-batch-processing
        """
        response = self._post(path='/do/batchCreate', params=kwargs)
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
    
    def read_by_fid(self, fid=None, **kwargs):
        """
        Returns data for the prospect specified by <fid>. <fid> must be a valid CRM FID.
        This data includes campaign assignment, profile criteria matching statuses, associated
        visitor activities, email list subscriptions, and custom field data. <id> is the Pardot
        ID of the target prospect.
        """
        if not fid:
            raise PardotAPIArgumentError('CRM FID is required.')
        response = self._post(path='/do/read/fid/{fid}'.format(fid=fid), params=kwargs)
        return response

    def update_by_fid(self, fid=None, **kwargs):
        """
        Updates the provided data for a prospect specified by <fid>. <fid> is the Pardot CRM FID of the
        prospect. Fields that are not updated by the request remain unchanged.
        """
        if not fid:
            raise PardotAPIArgumentError('CRM FID is required to update a prospect.')
        response = self._post(path='/do/update/fid/{fid}'.format(fid=fid), params=kwargs)
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

    def batchUpdate(self, **kwargs):
        """
        Updates prospects using the provided <data> in either XML or JSON.
        See Endpoints for Batch Processing: http://developer.pardot.com/kb/api-version-4/prospects/#endpoints-for-batch-processing
        """
        response = self._post(path='/do/batchUpdate', params=kwargs)
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

    def upsert_by_fid(self, fid=None, **kwargs):
        """
        Updates the provided data for the prospect specified by <fid>. If an <email> value is provided, it is used to
        update the prospect's email address. If a prospect with the provided ID is not found, Pardot searches for a
        prospect identified by <email>. If a prospect with the provided email address does not yet exist, a new
        prospect is created using <email> value. Fields that are not updated by the request remain unchanged.
        """
        if not fid:
            raise PardotAPIArgumentError('CRM FID is required to upsert a prospect.')
        response = self._post(path='/do/upsert/fid/{fid}'.format(fid=fid), params=kwargs)
        return response

    def batchUpsert(self, **kwargs):
        """
        Updates prospects using the provided <data> in either XML or JSON.
        See Endpoints for Batch Processing: http://developer.pardot.com/kb/api-version-4/prospects/#endpoints-for-batch-processing
        """
        response = self._post(path='/do/batchUpsert', params=kwargs)

    def delete_by_fid(self, fid=None, **kwargs):
        """Deletes the prospect specified by <fid>. Returns True if operation was successful."""
        if not fid:
            raise PardotAPIArgumentError('CRM FID is required to delete a prospect.')
        response = self._post(path='/do/delete/fid/{fid}'.format(fid=fid), params=kwargs)
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

    def update_field_by_fid(self, fid=None, field_name=None, field_value=None):
        """Updates the provided field for the prospect specified by <fid>. Returns the updated prospect."""
        response = self.update_by_fid(fid=fid, **{field_name: field_value})
        return response

    def read_field_by_fid(self, fid=None, field_name=None):
        """Returns the value of the provided field for the prospect specified by <fid>."""
        response = self.read_by_fid(fid=fid)
        return response.get('prospect').get(field_name)

    def read_field_by_id(self, id=None, field_name=None):
        """Returns the value of the provided field for the prospect specified by <id>."""
        response = self.read_by_id(id=id)
        return response.get('prospect').get(field_name)

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