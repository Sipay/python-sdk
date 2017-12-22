"""Response module."""


class Response:
    """Response class."""

    def __init__(self, response):
        """Initilize."""
        self.code = int(response['code'])
        self.detail = response['detail']
        self.description = response['description']
        self.request_id = response['request_id']
        self.type = response['type']
        self.uuid = response['uuid']

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid)
        return '<Response(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5})>'.format(*args)
