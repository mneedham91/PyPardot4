class PardotAPIError(Exception):
    """
    Basic exception class for errors encountered in API post and get requests. Takes the json response and parses out
    the error code and message.
    """

    def __init__(self, json_response):
        self.response = json_response
        self.err_code = json_response.get('@attributes').get('err_code')
        self.message = str(json_response.get('err'))
        if self.err_code is None:
            self.err_code = 0
            self.message = 'Unknown API error occurred'

    def __str__(self):
        return 'Error #{err_code}: {message}'.format(err_code=self.err_code, message=self.message)


class PardotAPIArgumentError(Exception):
    pass
