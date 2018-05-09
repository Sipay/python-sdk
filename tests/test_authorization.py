import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.authorization import Authorization

from sipay.paymethod.card import Card


class AuthorizationTests(unittest.TestCase):

    def setUp(self):
        self.ecommerce = Ecommerce('etc/config.ini')

        self.amount = Amount(100, 'EUR')

        self.card = Card('4242424242429942', 2050, 1)

        self.auth = self.ecommerce.authorization(self.card, self.amount)

    def test_init_authorization(self):

        self.assertIsInstance(self.auth, Authorization)
