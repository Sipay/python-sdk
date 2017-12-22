"""MaskedCard module."""
from mdwr.responses import Response
from datetime import datetime
from mdwr.paymethod.card import Card


class MaskedCard(Response):
    """MaskedCard class."""

    def __init__(self, response):
        """Initialize."""
        super().__init__(response)
        payload = response['payload']
        self.expired_at = payload.get('expired_at')
        self.card = payload.get('token')
        self.internal_code = payload.get('code')
        self.card_mask = payload.get('card_mask')
        self.token = payload.get('token')

        if self.expired_at:
            date = datetime.strptime(payload['expired_at'], '%Y-%m-%d').date()
            self.expired_at = date

        if self.card:
            self.card = Card(self.card)

        if self.internal_code:
            self.internal_code = int(self.internal_code)

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid, self.expired_at, self.card,
                self.internal_code, self.card_mask, self.token)
        return '<MaskedCard(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5}, expired_at={6}, card={7},'\
               ' internal_code={8}, card_mask={9}, token={10})>'.format(*args)
