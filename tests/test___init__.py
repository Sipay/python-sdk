from sipay import Ecommerce
from configparser import ConfigParser
import unittest


class InitTests(unittest.TestCase):

    def setUp(self):
        self.config_file = 'etc/config.ini'
        self.ecommerce = Ecommerce(self.config_file)
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.cred = self.config['credentials']

    def test_init(self):
        self.assertIsInstance(self.ecommerce, Ecommerce)
        self.assertIsInstance(self.config_file, str)
        with self.assertRaises(TypeError):
            Ecommerce(3)
