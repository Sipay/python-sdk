import unittest
from sipay.amount import Amount


class AmountTests(unittest.TestCase):

    def setUp(self):
        self.amount1 = Amount(100, 'EUR')
        self.amount3 = Amount(100, 'EUR')
        self.amount2 = Amount(200, 'EUR')
        self.amount4 = Amount(300, 'TRY')
        self.amount5 = Amount('300.00', 'USD', ',')

    def test_init_amount(self):
        with self.assertRaises(TypeError):
            self.amount5 = Amount('300.00', 'USD', '#', '.')
        with self.assertRaises(TypeError):
            self.amount5 = Amount('300.00', 'USD', '.', '$')
        with self.assertRaises(TypeError):
            self.amount5 = Amount('300.00', 'USD', '.', '.')
        self.assertTrue(len(self.amount5.separator), 1)

    def test_get_set_currency(self):
        self.assertEqual(self.amount1.currency, 'EUR')
        self.amount4.currency = 'TND'
        self.assertEqual(self.amount4.currency, 'TND')
        with self.assertRaises(ValueError):
            self.amount4.currency = 'ASD'
        with self.assertRaises(TypeError):
            self.amount4.currency = 1

    def test_get_set_amount(self):
        self.assertEqual(self.amount1.amount, 100)
        self.amount4.amount = 500
        self.assertEqual(self.amount4.amount, 500)
        with self.assertRaises(ValueError):
            self.amount4.amount = -1
        with self.assertRaises(TypeError):
            self.amount4.amount = 'something'

    def test_amount_gt_amount(self):
        self.assertFalse(self.amount1 > self.amount2)
        self.assertTrue(self.amount2 > self.amount1)
        with self.assertRaises(TypeError):
            self.amount1 > self.amount4
        with self.assertRaises(TypeError):
            self.amount1 > 'something'

    def test_amount_lt_amount(self):
        self.assertTrue(self.amount1 < self.amount2)
        self.assertFalse(self.amount2 < self.amount1)
        with self.assertRaises(TypeError):
            self.amount1 < self.amount4
        with self.assertRaises(TypeError):
            self.amount1 < 'something'

    def test_amount_add_amount(self):
        result = self.amount1 + self.amount2
        self.assertIsInstance(result, Amount)
        self.assertEqual(result.amount, 300)
        self.assertEqual(result.currency, 'EUR')
        with self.assertRaises(TypeError):
            self.amount1 + self.amount4
        with self.assertRaises(TypeError):
            self.amount1 + 'something'
        with self.assertRaises(TypeError):
            'something' + self.amount1

    def test_amount_sub_amount(self):
        result = self.amount2 - self.amount1
        self.assertIsInstance(result, Amount)
        self.assertEqual(result.amount, 100)
        self.assertEqual(result.currency, 'EUR')
        with self.assertRaises(ValueError):
            self.amount1 - self.amount2
        with self.assertRaises(TypeError):
            self.amount1 - self.amount4
        with self.assertRaises(TypeError):
            self.amount1 - 'something'
        with self.assertRaises(TypeError):
            'something' - self.amount1

    def test_amount_ge_amount(self):
        self.assertTrue(self.amount2 >= self.amount1)
        self.assertFalse(self.amount1 >= self.amount2)
        self.assertTrue(self.amount1 >= self.amount3)
        with self.assertRaises(TypeError):
            self.amount1 >= self.amount4
        with self.assertRaises(TypeError):
            self.amount1 >= 'something'

    def test_amount_le_amount(self):
        self.assertFalse(self.amount2 <= self.amount1)
        self.assertTrue(self.amount1 <= self.amount2)
        self.assertTrue(self.amount1 <= self.amount3)
        with self.assertRaises(TypeError):
            self.amount1 <= self.amount4
        with self.assertRaises(TypeError):
            self.amount1 <= 'something'

    def test_amount_eq_amount(self):
        self.assertTrue(self.amount1 == self.amount3)
        self.assertFalse(self.amount1 == self.amount2)
        with self.assertRaises(TypeError):
            self.amount1 == self.amount4
        with self.assertRaises(TypeError):
            self.amount1 == 'something'

    def test_amount_uneq_amount(self):
        self.assertTrue(self.amount2 != self.amount1)
        self.assertFalse(self.amount1 != self.amount3)
        with self.assertRaises(TypeError):
            self.amount1 != self.amount4
        with self.assertRaises(TypeError):
            self.amount1 != 'something'

    def test_str(self):
        self.assertEqual(str(self.amount1), '1.00EUR')
