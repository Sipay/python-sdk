import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.unlock import Unlock


class UnlockTests(unittest.TestCase):

    def test_init_unlock(self):

        ecommerce = Ecommerce('etc/config.ini')

        amount = Amount(100, 'EUR')

        self.unlock = ecommerce.unlock('something', amount)

        self.assertIsInstance(self.unlock, Unlock)
