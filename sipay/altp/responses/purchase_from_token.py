"""Purchase from token module."""
from sipay.altp.responses import Response
import pprint


class Purchase_from_token(Response):
    """Purchase class."""
    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        pprint.pprint(response)
        if response.get('payload'):
            payload = response['payload']
            self.final = payload.get('final')
            self.status = payload.get('status')
            self.request_id = payload.get('request_id')
            self.transaction_id = payload.get('transaction_id')
            self.response_type = payload.get('response_type')
            self.auth_token = payload.get('auth_token')
            self.purchase_code = payload.get('purchase_code')
            self.amount = payload.get('amount')
