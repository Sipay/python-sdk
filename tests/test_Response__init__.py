import unittest

from sipay.ecommerce.responses import Response


class ResponseTests(unittest.TestCase):

    def setUp(self):

        respose = {
            'code': '',
            'detail': '',
            'description': '',
            'request_id': '',
            'type': '2017-02-27',
            "uuid": "14:54:31",
        }

        request = {}

        self.resp = Response(request, respose)

    def test_init_response(self):

        self.assertIsInstance(self.resp, Response)

    def test_str_(self):
        self.assertIsInstance(self.resp.__str__(), str)
