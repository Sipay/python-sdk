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
            self.transactions = [Transaction(tx) for tx in payload['items']]

        else:
            self.transactions = None
