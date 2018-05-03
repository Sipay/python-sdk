import unittest
from sipay.paymethod.fastpay import FastPay


class FastPayTests(unittest.TestCase):

    def setUp(self):
        self.fp = FastPay('12345678901234567890123456789011')

    def test_init_fastpay(self):
        with self.assertRaises(TypeError):
            fp = FastPay(12345678901234567890123456789011)
        with self.assertRaises(ValueError):
            fp = FastPay('123456789012345678901234567890')

    def test_get_set_token(self):
        self.assertEqual(self.fp.token, '12345678901234567890123456789011')
        self.fp.token = '12345678901234567890123456789099'
        self.assertEqual(self.fp.token, '12345678901234567890123456789099')
        with self.assertRaises(TypeError):
            self.fp.token = 12345678901234567890123456789011
        with self.assertRaises(ValueError):
            self.fp.token = '123456789012345678901234567890'

    def test_to_dict(self):
        self.fp = FastPay('12345678901234567890123456789011')
        self.assertIsInstance(self.fp, FastPay)
        self.assertEqual(self.fp.token, '12345678901234567890123456789011')

if __name__ == '__main__':
    unittest.main()
