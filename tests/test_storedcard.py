import unittest
from sipay.paymethod.storedcard import StoredCard


class StoredCardTests(unittest.TestCase):

    def setUp(self):
        self.storedcard = StoredCard('token-card')

    def test_init_storedcard(self):
        with self.assertRaises(ValueError):
            StoredCard('token')
        with self.assertRaises(TypeError):
            StoredCard(123)

    def test_get_set_token(self):
        self.assertEqual(self.storedcard.token, 'token-card')
        self.storedcard.token = 'token-card-2'
        self.assertEqual(self.storedcard.token, 'token-card-2')
        with self.assertRaises(ValueError):
            self.storedcard.token = 'token'
        with self.assertRaises(TypeError):
            self.storedcard.token = 123

    def test_to_dict(self):
        self.assertEqual(self.storedcard.to_dict(), {'token': 'token-card'})
