import json

class Import(object):
    """
    A class to query and use Pardot Import API.
    Import API reference: https://developer.pardot.com/kb/api-version-3/import/
    """

    def __init__(self, client):
        self.client = client

    def create(self, file_name=None, **kwargs):
        """Creates a new asynchronous import.
        A single part with the name "importFile" should contain the CSV file for the batch. The file should contain a header row.
        Prarams(as importInput if file_name is not null):
        {
          "operation": "Upsert",
          "object": "Prospect",
          "state": "Ready"
        }
        """
        if not file_name:
            headers = {"Content-Type": "application/json"}
            response = self._post(path='/do/create', json=kwargs, headers=headers)
            return response

        with open(file_name, "rb") as f:
            files = {"importFile": f}
            params = {"importInput": json.dumps(kwargs)}
            response = self._post(path='/do/create',
                                  params=params,
                                  files=files)
        return response

    def add_batch(self, id, file_name, **kwargs):
        """Allows adding batches of data to an existing import when in the "Open" state.
        A single part with the name "importFile" should contain the CSV file for the batch. The file should contain a header row.
        """
        with open(file_name, "rb") as f:
            files = {"importFile": f}
            response = self._post(path='/do/batch/id/{id}'.format(id=id),
                                  params=kwargs,
                                  files=files)

        return response

    def update(self, id=None, **kwargs):
        """Used to submit the import by changing the state to "Ready". After this step, no more batches of data can be added, and processing of the import begins.
        """
        headers = {"Content-Type": "application/json"}
        response = self._patch(path='/do/update/id/{id}'.format(id=id),
                               json=kwargs, headers=headers)
        return response

    def read(self, id=None, **kwargs):
        """Returns the current state of the import. If processing is complete, the output provides a path to the results of the operation along with any statistics about the operation.
        """
        response = self._get(path='/do/read/id/{id}'.format(id=id), params=kwargs)
        return response

    def query(self, **kwargs):
        """Used by administrators to retrieve a list of imports and their status. A user must have the “Admin > Imports > View” ability to execute this endpoint.
        """
        response = self._get(path='/do/query', params=kwargs)

        # Ensure result['prospectAccount'] is a list, no matter what.
        result = response.get('result')
        if result['total_results'] == 0:
            result['import'] = []
        elif result['total_results'] == 1:
            result['import'] = [result['import']]

        return result

    def download_errors(self, **kwargs):
        """Download errors associated with the specified import (after it is complete).
        """
        response = self._get(path='/do/downloadErrors/id/{id}'.format(id=id), params=kwargs)
        return response

    def _get(self, object_name='import', path=None, params=None):
        """GET requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='import', path=None, params=None,
              headers=None, json=None, files=None):
        """POST requests for the Account object."""
        response = self.client.post(object_name=object_name, path=path,
                                    params=params, headers=headers,
                                    json=json, files=files)
        return response

    def _patch(self, object_name='import', path=None, params=None,
              headers=None, json=None, files=None):
        """POST requests for the Account object."""
        response = self.client.patch(object_name=object_name, path=path,
                                     params=params, headers=headers,
                                     json=json, files=files)
        return response
