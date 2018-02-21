class Emails(object):
    """
    A class to query and send Pardot emails.
    Email field reference: http://developer.pardot.com/kb/object-field-references/#email
    """

    def __init__(self, client):
        self.client = client

    def send_to_email(self, prospect_email=None, **kwargs):
        """
        Sends an email to the prospect identified by <prospect_email>.
        Required parameters: (email_template_id OR (text_content, name, subject, & ((from_email & from_name) OR from_user_id)))
        """
        response = self._post(
            path='/do/send/prospect_email/{prospect_email}'.format(prospect_email=prospect_email),
            params=kwargs)
        return response

    def send_to_id(self, prospect_id=None, **kwargs):
        """
        Sends an email to the prospect identified by <prospect_id>.
        Required parameters: (email_template_id OR (text_content, name, subject, & ((from_email & from_name) OR from_user_id)))
        """
        response = self._post(
            path='/do/send/prospect_id/{prospect_id}'.format(prospect_id=prospect_id), params=kwargs)
        return response

    def send_to_lists(self, **kwargs):
        """
        Sends an email to the lists identified by list_ids[].
        Required parameters: (email_template_id OR (text_content, name, subject, & ((from_email & from_name) OR from_user_id)))
        """
        kwargs['list_ids'] = kwargs.get('list_ids', None)
        response = self._post(
            path='/do/send/', params=kwargs)
        return response

    def read(self, email_id=None):
        """Returns the data for the email specified by <email_id>. <email_id> is the Pardot ID of the target email."""
        response = self._post(path='/do/read/id/{email_id}'.format(email_id=email_id))
        return response
    
    def stats(self, list_email_id=None):
        """Returns the statistical data for the list email specified by <list_email_id>. <list_email_id> is the Pardot ID of the target email."""
        response = self._post(path='/do/stats/id/{list_email_id}'.format(list_email_id=list_email_id))
        return response

    def _get(self, object_name='email', path=None, params=None):
        """GET requests for the Email object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='email', path=None, params=None):
        """POST requests for the Email object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
