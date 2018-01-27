from ..errors import PardotAPIArgumentError


class EmailTemplates(object):
    """
    A class to query and use Pardot email templates.
    """

    def __init__(self, client):
        self.client = client

    def read(self, emailTemplateID=None, **kwargs):
        """
        Returns the data for the email template specified by <id>. <id> is the Pardot ID of the target email template.
        """
        if not emailTemplateID:
            raise PardotAPIArgumentError('email template id is required to read an email template.')
        response = self._post(path='/do/read/id/{emailTemplateID}'.format(emailTemplateID=emailTemplateID), params=kwargs)
        return response

    def listOneToOne(self, **kwargs):
        """
        Returns a list of email templates which are enabled for use in one to one emails.
        """
        response = self._post(path='/do/listOneToOne', params=kwargs)
        return response

    def _get(self, object_name='emailTemplate', path=None, params=None):
        """GET requests for the email template object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='emailTemplate', path=None, params=None):
        """POST requests for the email template object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
