import unittest

from sipay import Ecommerce

from sipay.ecommerce.responses.card import Card


class CardTests(unittest.TestCase):

    def test_init_CardResponse(self):

        ecommerce = Ecommerce('etc/config.ini')
        self.card = ecommerce.card("newtoken")
        self.assertIsInstance(self.card, Card)
