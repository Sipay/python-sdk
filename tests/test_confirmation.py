import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.confirmation import Confirmation


class ConfirmationTests(unittest.TestCase):

    def setUp(self):

        ecommerce = Ecommerce('etc/config.ini')

        amount = Amount(100, 'EUR')

        self.conf = ecommerce.confirmation('something', amount)

    def test_init_confirmation(self):

        self.assertIsInstance(self.conf, Confirmation)
