import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.unlock import Unlock


class UnlockTests(unittest.TestCase):

    def setUp(self):

        self.payload = {
            'amount': 100,
            'currency': 'EUR'
        }
        self.amount = Amount(self.payload['amount'], self.payload['currency'])

    def test_init_unlock(self):

        ecommerce = Ecommerce('etc/config.ini')

        amount = Amount(100, 'EUR')

        self.unlock = ecommerce.unlock('something', amount)

        self.assertIsInstance(self.unlock, Unlock)

    def test_init2test_init_unlock(self):

        self.assertIn('amount', self.payload)
        self.assertIn('currency', self.payload)
        self.assertEqual(self.payload['amount'], self.amount.amount)
        self.assertEqual(self.payload['currency'], self.amount.currency)
