import unittest

from sipay import Ecommerce

from sipay.ecommerce.responses.query import Query


class QueryTests(unittest.TestCase):

    def test_init_query(self):
        ecommerce = Ecommerce('etc/config.ini')
        self.query = ecommerce.query("something")

        self.assertIsInstance(self.query, Query)
