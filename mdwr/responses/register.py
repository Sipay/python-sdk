"""Register module."""
from mdwr.responses import Response
from datetime import datetime
from mdwr.paymethod.tokenizedcard import TokenizedCard


class Register(Response):
    """Register class."""

    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        payload = response['payload']
        self.expired_at = payload.get('expired_at')
        self.card_mask = payload.get('card_mask')
        self.token = payload.get('token')
        self.card = self.token = payload.get('token')

        if self.expired_at:
            date = datetime.strptime(payload['expired_at'], '%Y-%m-%d').date()
            self.expired_at = date

        if self.card:
            self.card = TokenizedCard(self.card)

    def __str__(self):
        """Cast to string."""
        args = (self.code, self.detail, self.description, self.request_id,
                self.type, self.uuid, self.expired_at, self.card, self.card_mask, self.token)
        return '<MaskedCard(code={0}, detail={1}, description={2}, '\
               'request_id={3}, type={4}, uuid={5}, expired_at={6}, card={7},'\
               ' card_mask={8}, token={9})>'.format(*args)
