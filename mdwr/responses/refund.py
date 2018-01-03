"""Refund module."""
from mdwr.responses import Response
from mdwr.amount import Amount


class Refund(Response):
    """Refund class."""

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

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid, self.approval,
                self.authorizator, self.card_trade, self.card_type, self.order,
                self.reconciliation, self.transaction_id)
        return '<Refund(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5}, approval={6}, '\
               'authorizator={7}, card_trade={8}, card_type={9}, '\
               'order={10}, reconciliation={11}, '\
               'transaction_id={12})>'.format(*args)
