"""Card file."""
from mdwr.paymethod import PayMethod
import re


class Card(PayMethod):
    """Card class."""

    def __init__(self, card_id):
        """Initialize.

        You can initialize a Card with:
            3-tupla (pan, year, month)
            string of token of card

        """
        self.card_id = card_id

    @property
    def card_id(self):
        """Getter of card_id."""
        return self._card_id

    @card_id.setter
    def card_id(self, card_id):
        token_type = isinstance(card_id, str)

        tuple_type = isinstance(card_id, tuple) and \
            isinstance(card_id[0], str) and isinstance(card_id[1], int) and \
            isinstance(card_id[2], int)

        if not token_type and not tuple_type:
            raise TypeError('card_id dont have a correct type.')

        if token_type:
            value_val = re.match(r'^[\w-]{6,128}$', card_id)

        if tuple_type:
            value_val = re.match(r'^[\w-]{14,19}$', card_id[0]) and \
                (2017 < card_id[1] <= 9999) and (0 < card_id[2] <= 12)

        if not value_val:
            raise ValueError('card_id dont have a correct value.')

        self._card_id = card_id

    def add_to(self, payload):
        """Add to payload a card."""
        if isinstance(self.card_id, tuple):
            payload['pan'], payload['year'], payload['month'] = self.card_id

        if isinstance(self.card_id, str):
            payload['token'] = self.card_id
