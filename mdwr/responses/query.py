"""Query module."""
from mdwr.responses import Response
from mdwr.responses.transaction import Transaction


class Query(Response):
    """Query class."""

    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        payload = response['payload']
        if payload:
            self.internal_code = int(payload['code'])
            self.transactions = [Transaction(tx) for tx in payload['items']]

        else:
            self.internal_code = None
            self.transactions = None

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid, self.internal_code)
        return '<Query(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5}, '\
               'internal_code={6})>'.format(*args)
