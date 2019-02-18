import unittest

from sipay import Ecommerce

from sipay.ecommerce.responses.register import Register

from sipay.paymethod.card import Card


class RegisterTests(unittest.TestCase):

    def test_init_Unregister(self):
        ecommerce = Ecommerce('etc/config.ini')

        card = Card('4242424242424242', 2050, 1)

        self.reg = ecommerce.register(card, 'newtoken')

        self.assertIsInstance(self.reg, Register)
