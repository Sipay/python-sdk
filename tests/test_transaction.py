import unittest

from sipay.ecommerce.responses.transaction import Transaction


class TransactionTests(unittest.TestCase):

    def setUp(self):

        data = {
            'channel_name': '',
            'channel': '',
            'method': '',
            'date': '2017-02-27',
            "time": "14:54:31",
            'order': '',
            'transaction_id': '',
            'code': '',
            'method_name': '',
            'operation': '',
            'amount': 123,
            'currency': 'EUR',
            'authorization_id': '',
            'description': '',
            'masked_card': '',
            'operation_name': '',
            'status': '',
        }

        self.transa = Transaction(data)

    def test_init_transaction(self):

        self.assertIsInstance(self.transa, Transaction)

    def test_str_(self):
        self.assertIsInstance(self.transa.__str__(), str) 
