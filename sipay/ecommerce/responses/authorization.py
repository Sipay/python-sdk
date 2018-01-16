"""Authorization module."""
from sipay.ecommerce.responses import Response
from sipay.amount import Amount


class Authorization(Response):
    """Authorization class."""

    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        payload = response['payload']
        self.approval = payload.get('approval')
        self.authorizator = payload.get('authorizator')
        self.card_trade = payload.get('card_trade')
        self.card_type = payload.get('card_type')
        self.masked_card = payload.get('masked_card')
        self.order = payload.get('order')
        self.reconciliation = payload.get('reconciliation')
        self.transaction_id = payload.get('transaction_id')

        if payload.get('amount') and payload.get('currency'):
            self.amount = Amount(payload['amount'], payload['currency'])

        else:
            self.amount = None
