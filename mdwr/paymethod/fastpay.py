"""FastPay file."""
from mdwr.paymethod import PayMethod
import re


class FastPay(PayMethod):
    """FastPay class."""

    def __init__(self, token):
        """Initialize."""
        self.token = token

    @property
    def token(self):
        """Getter of token."""
        return self._token

    @token.setter
    def token(self, token):
        if not isinstance(token, str):
            raise TypeError('token must be a string.')

        if not re.match(r'^[0-9a-fA-F]{32}$', token):
            raise ValueError('token must have 32 hexadecimal characters.')

        self._token = token

    def add_to(self, payload):
        """Add to payload a FastPay."""
        payload['fastpay'] = {'request_id': self.token}
