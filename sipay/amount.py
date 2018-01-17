"""Amount module."""
from sipay.catalogs.currency import CURRENCIES
import re


class Amount:
    """Amount class."""

    def __init__(self, amount, currency):
        """Initialize Amount."""
        self.currency = currency
        index = -self._currency[2]-1
        if isinstance(amount, str) and \
           re.match(r'^([0-9]+\.[0-9]+)$', amount) and amount[index] == '.':
            amount = amount.replace('.', '')
            amount = int(amount)

        self.amount = amount

    @property
    def currency(self):
        """Getter of currency."""
        return self._currency[0]

    @currency.setter
    def currency(self, currency):
        if not isinstance(currency, str):
            raise TypeError('currency must be a string.')

        if currency not in CURRENCIES:
            raise ValueError('value of currency is incorrect.')

        self._currency = CURRENCIES[currency]

    @property
    def amount(self):
        """Getter of amount."""
        return self._amount

    @amount.setter
    def amount(self, amount):
        if not isinstance(amount, int):
            raise TypeError('amount must have a correct format.')

        if amount <= 0:
            raise ValueError('value of amount is incorrect.')

        self._amount = amount

    def __add__(self, other):
        """Operator +."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return Amount(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        """Operator -."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return Amount(self.amount - other.amount, self.currency)

    def __gt__(self, other):
        """Operator >."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount > other.amount

    def __lt__(self, other):
        """Operator <."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount < other.amount

    def __ge__(self, other):
        """Operator >=."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount >= other.amount

    def __le__(self, other):
        """Operator <=."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount <= other.amount

    def __eq__(self, other):
        """Operator ==."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount == other.amount

    def __ne__(self, other):
        """Operator !=."""
        if not isinstance(other, Amount):
            raise TypeError('Second argument must be a Amount.')

        if self.currency != other.currency:
            raise TypeError('You can not add two amounts with different currencies.')  # noqa

        return self.amount != other.amount

    def __str__(self):
        """Parse to string."""
        dec = self._currency[2]
        fmt_amount = str(self.amount).zfill(dec + 1)
        return fmt_amount[:-dec] + '.' + fmt_amount[-dec:] + self.currency
