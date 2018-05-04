import unittest
from sipay.paymethod.fastpay import FastPay

FASTPAY = '12345678901234567890123456789011'


class FastPayTests(unittest.TestCase):

    def setUp(self):
        self.fp = FastPay(FASTPAY)

    def test_init_fastpay(self):
        with self.assertRaises(TypeError):
            FastPay(12345678901234567890123456789011)
        with self.assertRaises(ValueError):
            FastPay('123456789012345678901234567890')

    def test_get_set_token(self):
        self.assertEqual(self.fp.token, FASTPAY)
        self.fp.token = '12345678901234567890123456789099'
        self.assertEqual(self.fp.token, '12345678901234567890123456789099')
        with self.assertRaises(TypeError):
            self.fp.token = 12345678901234567890123456789011
        with self.assertRaises(ValueError):
            self.fp.token = '123456789012345678901234567890'

    def test_to_dict(self):
        self.assertEqual(self.fp.to_dict(), {'fastpay': {'request_id': FASTPAY}})  # noqa
