"""Unlock module."""
from sipay.ecommerce.responses import Response
from sipay.amount import Amount


class Unlock(Response):
    """Preauthorization class."""

    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        payload = response['payload']
        self.order = payload.get('order')
        self.reconciliation = payload.get('reconciliation')
        self.transaction_id = payload.get('transaction_id')

        if payload.get('amount') and payload.get('currency'):
            self.amount = Amount(payload['amount'], payload['currency'])

        else:
            self.amount = None
