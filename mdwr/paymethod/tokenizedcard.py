"""Card file."""
from mdwr.paymethod import PayMethod
import re


class TokenizedCard(PayMethod):
    """TokenizedCard class."""

    def __init__(self, token):
        """Initialize.

        string of token of card
        """
        self.token = token

    @property
    def token(self):
        """Getter of token."""
        return self._token

    @token.setter
    def token(self, token):
        if not isinstance(token, str):
            raise TypeError('token dont have a correct type.')

        if not re.match(r'^[\w-]{6,128}$', token):
            raise ValueError('token dont have a correct value.')

        self._token = token

    def add_to(self, payload):
        """Add to payload a card."""
        payload['token'] = self.token
