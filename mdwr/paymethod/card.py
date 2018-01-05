"""Card file."""
from mdwr.paymethod import PayMethod
import re
import time


class Card(PayMethod):
    """Card class."""

    def __init__(self, card_number, year, month):
        """Initialize."""
        self.card_number = card_number
        self.set_expiration_date(year, month)

    @property
    def card_number(self):
        """Getter of card_number."""
        return self._card_number

    @card_number.setter
    def card_number(self, card_number):
        if not isinstance(card_number, str):
            raise TypeError('card_number hasn\'t a correct type.')

        if not re.match(r'^[\w-]{14,19}$', card_number):
            raise ValueError('card_number hasn\'t a correct value.')

        self._card_number = card_number

    @property
    def year(self):
        """Getter of year."""
        return self._year

    @property
    def month(self):
        """Getter of month."""
        return self._month

    def set_expiration_date(self, year, month):
        """Set expiration date."""
        if not isinstance(year, int):
            raise TypeError('year hasn\'t a correct type.')

        if not (999 < year <= 9999):
            raise ValueError('year hasn\'t a correct value.')

        self._year = year

        if not isinstance(month, int):
            raise TypeError('month hasn\'t a correct type.')

        if not (0 < month <= 12):
            raise ValueError('month hasn\'t a correct value.')

        self._month = month

        if self.is_expired():
            raise Exception('Card is expired.')

    def is_expired(self):
        """Return if card is expired."""
        year, month, _, _, _, _, _, _, _ = time.localtime()
        return self.year < year or (self.year == year and self.month < month)

    def to_dict(self):
        """Parse card date to dict."""
        return {
            'pan': self.card_number,
            'year': self.year,
            'month': self.month
        }
