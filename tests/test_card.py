import unittest
from sipay.paymethod.card import Card


class CardTests(unittest.TestCase):

    def setUp(self):
        self.card = Card('6712009000000205', 2050, 1)

    def test_init_card(self):
        with self.assertRaises(TypeError):
            Card('6712009000000205')
        with self.assertRaises(TypeError):
            Card('671200900000020')
        with self.assertRaises(TypeError):
            Card('671200900000020W')
        with self.assertRaises(TypeError):
            Card('6712009000000205', 2050)
        with self.assertRaises(TypeError):
            Card('6712009000000205', 'something', 1)
        with self.assertRaises(TypeError):
            Card('6712009000000205', '', 1)
        with self.assertRaises(TypeError):
            Card('6712009000000205', 2050, '1')

    def test_get_set_card(self):
        self.assertEqual(self.card.card_number, '6712009000000205')
        with self.assertRaises(TypeError):
            self.card.card_number = 1
        with self.assertRaises(ValueError):
            self.card.card_number = '1'

    def test_get_set_year_month(self):
        self.assertEqual(self.card.year, 2050)
        self.assertEqual(self.card.month, 1)
        self.card.set_expiration_date(2049, 2)
        self.assertEqual(self.card.year, 2049)
        self.assertEqual(self.card.month, 2)
        with self.assertRaises(ValueError):
            self.card.set_expiration_date(998, 2)
        with self.assertRaises(TypeError):
            self.card.set_expiration_date(998.00, 2)
        with self.assertRaises(ValueError):
            self.card.set_expiration_date(1000, 13)
        with self.assertRaises(TypeError):
            self.card.set_expiration_date(1000, 2.00)
        with self.assertRaises(Exception):
            self.card.set_expiration_date(1999, 1)

    def test_is_expired(self):
        with self.assertRaises(Exception):
            Card('6712009000000205', 2018, 3)
