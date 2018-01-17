"""Card module."""
from sipay.ecommerce.responses import Response
from datetime import datetime
from sipay.paymethod.storedcard import StoredCard


class Card(Response):
    """Card class."""

    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        payload = response['payload']
        self.expired_at = payload.get('expired_at')
        self.card = None
        self.card_mask = payload.get('card_mask')
        self.token = payload.get('token')

        if self.expired_at:
            date = datetime.strptime(payload['expired_at'], '%Y-%m-%d').date()
            self.expired_at = date

        if self.token:
            self.card = StoredCard(self.token)
