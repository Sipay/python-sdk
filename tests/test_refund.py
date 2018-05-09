import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.refund import Refund


class RefundTests(unittest.TestCase):

    def setUp(self):

        ecommerce = Ecommerce('etc/config.ini')

        amount = Amount(100, 'EUR')

        self.refund = ecommerce.refund('something', amount)

    def test_init_refund(self):

        self.assertIsInstance(self.refund, Refund)
