"""Card file."""
from sipay.paymethod import PayMethod
import re


class StoredCard(PayMethod):
    """StoredCard class."""

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
            raise TypeError('token doesn\'t have a correct type.')

        if not re.match(r'^[\w-]{6,128}$', token):
            raise ValueError('token doesn\'t have a correct value.')

        self._token = token

    def to_dict(self):
        """Parse card date to dict."""
        return {
            'token': self.token
        }
