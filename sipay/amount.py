"""Amount module."""
from sipay.catalogs.currency import CURRENCIES
import re

THOUSAND_SEPARATORS = (',', ' ', '\'', '.', '')
DECIMAL_SEPARATORS = (',', '.')


class Amount:
    """Amount class."""

    def __init__(self, amount, currency, separator='', decimal_separator='.'):
        """Initialize Amount."""
        self.currency = currency
        self.separator = separator
        self.decimal_separator = decimal_separator

        if not isinstance(separator, str) or \
           separator not in THOUSAND_SEPARATORS:
            raise TypeError('separator must be [ ,\'.].')

        if not isinstance(decimal_separator, str) or \
           decimal_separator not in DECIMAL_SEPARATORS:
            raise TypeError('decimal_separator must be [,.]')

        if decimal_separator == separator:
            raise TypeError('separators are equals.')

        if isinstance(amount, str):
            if len(separator) == 1:
                separator = "\{}".format(separator)

            decimal_separator = "\{}".format(decimal_separator)

            regex = '^[0-9]{{1,3}}({sep}[0-9]{{3}})*{decimal_sep}[0-9]'\
                    '{{{decimals}}}$'.format(sep=separator,
                                             decimal_sep=decimal_separator,
                                             decimals=self._currency[2])
            if re.match(regex, amount):
                amount = amount.replace(self.decimal_separator, '')
                amount = amount.replace(self.separator, '')
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
            raise TypeError('Second argument must be an Amount.')

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
        decimal = fmt_amount[-dec:]
        integer = fmt_amount[:-dec]
        length = len(integer)
        init = length % 3 if length % 3 > 0 else 3
        integer_ftm = integer[:init]

        for i in range(init, length, 3):
            integer_ftm += "{0}{1}".format(self.separator, integer[i:i+3])

        return integer_ftm + self.decimal_separator + decimal + self.currency
