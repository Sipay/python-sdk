"""FastPay file."""
from sipay.paymethod import PayMethod
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

    def to_dict(self):
        """Parse Fastpay date to dict."""
        return {
            'fastpay': {'request_id': self.token}
        }
