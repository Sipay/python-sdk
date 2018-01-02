"""Card file."""
from mdwr.paymethod import PayMethod
import re


class Card(PayMethod):
    """Card class."""

    def __init__(self, card_number, year, month):
        """Initialize."""
        self.card_number = card_number
        self.year = year
        self.month = month

    @property
    def card_number(self):
        """Getter of card_number."""
        return self._card_number

    @card_number.setter
    def card_number(self, card_number):
        if not isinstance(card_number, str):
            raise TypeError('card_number dont have a correct type.')

        if not re.match(r'^[\w-]{14,19}$', card_number):
            raise ValueError('card_number dont have a correct value.')

        self._card_number = card_number

    @property
    def year(self):
        """Getter of year."""
        return self._year

    @year.setter
    def year(self, year):
        if not isinstance(year, int):
            raise TypeError('year dont have a correct type.')

        if not (2017 < year <= 9999):
            raise ValueError('year dont have a correct value.')

        self._year = year

    def add_to(self, payload):
        """Add to payload a card."""
        payload['pan'] = self.card_number
        payload['year'] = self.year
        payload['month'] = self.month
