import unittest
from sipay.paymethod.card import Card

CARD = '4242424242424242'


class CardTests(unittest.TestCase):

    def setUp(self):
        self.card = Card(CARD, 2050, 1)

    def test_init_card(self):
        with self.assertRaises(TypeError):
            Card(CARD)

    def test_get_set_card(self):
        self.assertEqual(self.card.card_number, CARD)
        with self.assertRaises(TypeError):
            self.card.card_number = 1
        with self.assertRaises(ValueError):
            self.card.card_number = '1'

    def test_get_set_year_month(self):
        self.card.set_expiration_date(2049, 2)
        self.assertEqual(self.card.year, 2049)
        self.assertEqual(self.card.month, 2)
        with self.assertRaises(TypeError):
            self.card.set_expiration_date(998.00, 2)
        with self.assertRaises(ValueError):
            self.card.set_expiration_date(998, 2)
        with self.assertRaises(TypeError):
            self.card.set_expiration_date(1000, 2.00)
        with self.assertRaises(ValueError):
            self.card.set_expiration_date(1000, 13)
        with self.assertRaises(Exception):
            self.card.set_expiration_date(1999, 1)

    def test_is_expired(self):
        with self.assertRaises(Exception):
            Card(CARD, 2018, 3)

    def test_to_dict(self):
        self.assertEqual(self.card.to_dict(), {'pan': CARD, 'year': 2050, 'month': 1})  # noqa
