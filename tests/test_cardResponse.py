import unittest

from sipay import Ecommerce

from sipay.ecommerce.responses.card import Card

from sipay.paymethod.storedcard import StoredCard


class CardTests(unittest.TestCase):

    def setUp(self):
        self.payload = {
            'expired_at': ''
        }
        self.token = 'new-token'

    def test_init_CardResponse(self):

        ecommerce = Ecommerce('etc/config.ini')
        self.card = ecommerce.card("new-token")
        self.assertIsInstance(self.card, Card)
        self.assertIn('expired_at', self.payload)
        self.assertIsInstance(self.payload, dict)

        self.card = StoredCard(self.token)
        self.assertIsInstance(self.card, StoredCard)
