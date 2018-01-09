"""Response module."""


class Response:
    """Response class."""

    def __init__(self, request, response):
        """Initilize."""
        self.code = response.get('code')
        self.detail = response.get('detail')
        self.description = response.get('description')
        self.request_id = response.get('request_id')
        self.type = response.get('type')
        self.uuid = response.get('uuid')
        self._request = request
        self._response = response

        if self.code:
            self.code = int(self.code)

    def __str__(self):
        """Cast to string."""
        ret = ''
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                ret += '{0}={1}, '.format(k, v)

        ret = '<{0}({1})>'.format(type(self).__name__,ret[:-2])

        return ret
