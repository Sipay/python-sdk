"""Payment module."""
from sipay.altp.responses import Response


class Payment(Response):
    """Payment class."""
    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        if response.get('payload'):
            payload = response['payload']
            self.amount = payload.get('amount')
            self.currency = payload.get('currency')
            self.transaction_id = payload.get('transaction_id')
            self.datetime = payload.get('datetime')
            self.billing_id = payload.get('billing_id')
            self.status = payload.get('status')
            self.fee = payload.get('fee')
            self.payment_type = payload.get('payment_type')
