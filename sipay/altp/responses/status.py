"""Status module."""
from sipay.altp.responses import Response


class Status(Response):
    """Status class."""
    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        if response.get('payload'):
            payload = response['payload']
            request = payload['request']
            response = payload['response']
            self.order = request.get('order')
            self.status = payload.get('status')
            if response is not None:
                data = response.get('data')
                if data is not None:
                    self.currency = data.get('currency')
                    self.amount = data.get('amount')
                    self.payment_date = data.get('payment_date')
                    self.card = data['card']
                self.identifier = response.get('identifier')
                self.event = response.get('event')
                self.account_id = response.get('account_id')
