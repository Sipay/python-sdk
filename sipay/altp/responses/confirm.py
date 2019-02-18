"""Confirm module."""
from sipay.altp.responses import Response


class Confirm(Response):
    """Confirm class."""
    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        if response.get('payload'):
            payload = response['payload']
            self.token = payload.get('token')
            self.payment_info = payload.get('payment_info')
