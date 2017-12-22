"""Confirmation module."""
from mdwr.responses import Response


class Confirmation(Response):
    """Confirmation class."""

    def __init__(self, response):
        """Initialize."""
        super().__init__(response)
        payload = response['payload']
        self.internal_code = int(payload['code']) if payload else None

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid, self.internal_code)
        return '<Confirmation(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5}, '\
               'internal_code={6})>'.format(*args)
