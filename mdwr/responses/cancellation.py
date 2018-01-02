"""Cancellation module."""
from mdwr.responses import Response


class Cancellation(Response):
    """Cancellation class."""

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid)
        return '<Cancellation(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5})>'.format(*args)
