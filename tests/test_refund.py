import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.refund import Refund


class RefundTests(unittest.TestCase):

    def setUp(self):

        ecommerce = Ecommerce('etc/config.ini')

        self.amount = Amount(100, 'EUR')

        self.refund = ecommerce.refund('something', self.amount)

    def test_init_refund(self):

        self.assertIsInstance(self.refund, Refund)

        payload = {
            'amount': 100,
            'currency': 'EUR'
        }

        self.assertEqual(self.amount.amount, payload['amount'])
