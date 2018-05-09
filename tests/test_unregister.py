import unittest

from sipay import Ecommerce

from sipay.ecommerce.responses.unregister import Unregister


class Unregisterests(unittest.TestCase):

    def test_init_Unregister(self):
        ecommerce = Ecommerce('etc/config.ini')

        self.unreg = ecommerce.unregister("newtoken")

        self.assertIsInstance(self.unreg, Unregister)
