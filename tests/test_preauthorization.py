import unittest

from sipay import Ecommerce

from sipay.amount import Amount

from sipay.ecommerce.responses.preauthorization import Preauthorization

from sipay.paymethod.card import Card


class PreuthorizationTests(unittest.TestCase):

    def setUp(self):

        ecommerce = Ecommerce('etc/config.ini')

        amount = Amount(100, 'EUR')

        card = Card('4242424242424242', 2050, 1)

        self.preauth = ecommerce.preauthorization(card, amount)
        self.payload = {}

    def test_init_preauthorization(self):
        self.payload = {}
        self.assertIsInstance(self.preauth, Preauthorization)
        self.amount = None
        self.assertIsNone(self.amount)
