"""MDWR module."""
from configparser import ConfigParser
from time import time
from hashlib import sha256
from hashlib import sha512
import hmac
import json
import requests
import logging
import logger
import re

from mdwr.responses.operation import Operation
from mdwr.responses.confirmation import Confirmation
from mdwr.responses.masked_card import MaskedCard
from mdwr.responses.query import Query
from mdwr.paymethod import PayMethod


class MDWR:
    """SDK for using Sipay middleware easier."""

    def __init__(self, config_file):
        """Initialize MDWR with a config.ini file."""
        if not isinstance(config_file, str):
            self._logger.error('config_file must be a string.')
            raise TypeError('config_file must be a string.')

        config = ConfigParser()
        config.read(config_file)

        cred = config['credentials']
        self.key = cred.get('key', '')
        self.secret = cred.get('secret', '')
        self.resource = cred.get('resource', '')

        api = config['api']
        self.enviroment = api.get('enviroment', '')
        self.version = api.get('version', '')
        self.mode = api.get('mode', '')

        timeout = config['timeout']
        self.connection = timeout.getint('connection', 3)
        self.process = timeout.getint('process', 27)

        self._logger = self._get_logger(config['logger'])

    @property
    def key(self):
        """Getter of key."""
        return self._key

    @key.setter
    def key(self, key):
        if not isinstance(key, str):
            self._logger.error('key must be a string.')
            raise TypeError('key must be a string.')

        self._key = key

    @property
    def secret(self):
        """Getter of secret."""
        return self._secret

    @secret.setter
    def secret(self, secret):
        if not isinstance(secret, str):
            self._logger.error('secret must be a string.')
            raise TypeError('secret must be a string.')

        self._secret = secret

    @property
    def resource(self):
        """Getter of resource."""
        return self._resource

    @resource.setter
    def resource(self, resource):
        if not isinstance(resource, str):
            self._logger.error('Value of token is incorrect.')
            raise TypeError('resource must be a string.')

        self._resource = resource

    @property
    def enviroment(self):
        """Getter of enviroment."""
        return self._enviroment

    @enviroment.setter
    def enviroment(self, enviroment):
        if not isinstance(enviroment, str):
            self._logger.error('enviroment must be a string.')
            raise TypeError('enviroment must be a string.')

        # TODO: remove develop argument
        if enviroment not in ['develop', 'sandbox', 'staging', 'live']:
            self._logger.error('enviroment must be sandbox, staging or live')
            raise ValueError('enviroment must be sandbox, staging or live')

        self._enviroment = enviroment

    @property
    def mode(self):
        """Getter of mode."""
        return self._mode

    @mode.setter
    def mode(self, mode):
        if not isinstance(mode, str):
            self._logger.error('mode must be a string.')
            raise TypeError('mode must be a string.')

        if mode not in ['sha256', 'sha512']:
            self._logger.error('mode must be sha256 or sha512')
            raise ValueError('mode must be sha256 or sha512')

        self._mode = mode

    @property
    def version(self):
        """Getter of version."""
        return self._version

    @version.setter
    def version(self, version):
        if not isinstance(version, str):
            self._logger.error('version must be a string.')
            raise TypeError('version must be a string.')

        if version != 'v1':
            self._logger.error('version must be v1')
            raise ValueError('version must be v1')

        self._version = version

    @property
    def connection(self):
        """Getter of connection."""
        return self._connection

    @connection.setter
    def connection(self, connection):
        if not isinstance(connection, int):
            self._logger.error('connection must be a integer.')
            raise TypeError('connection must be a integer.')

        if connection <= 0:
            self._logger.error('connection must geater than 0.')
            raise ValueError('connection must geater than 0.')

        self._connection = connection

    @property
    def process(self):
        """Getter of process."""
        return self._process

    @process.setter
    def process(self, process):
        if not isinstance(process, int):
            self._logger.error('process must be a integer.')
            raise TypeError('process must be a integer.')

        if process <= 0:
            self._logger.error('process must geater than 0.')
            raise ValueError('process must geater than 0.')

        self._process = process

    def send(self, payload, endpoint):
        """Send payload to endpoint."""
        self.logger.info('Start send to endpoint ' + endpoint)
        nonce = str(time()).replace('.', '')
        secret = bytes(self.secret, 'utf-8')
        body_json = {
          'key': self.key,
          'resource': self.resource,
          'nonce': nonce,
          'mode': self.mode,
          'payload': payload
        }
        body_str = json.dumps(body_json)
        body = bytes(body_str, 'utf-8')
        method = {
            'sha256': sha256,
            'sha512': sha512
        }[self.mode]

        signature = hmac.new(secret, body, method).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Content-Signature': signature
        }
        url = 'https://{0}.sipay.es/mdwr/{1}/{2}'.format(self.enviroment,
                                                         self.version,
                                                         endpoint)

        try:
            r = requests.post(url, headers=headers, data=body_str)
            response = json.loads(r.content.decode('utf-8'))

        except Exception:
            self._logger.exception('Exception in post')
            response = None

        self.logger.info('End send to endpoint ' + endpoint)

        return response

    def _get_logger(self, config):
        """Set global logger."""
        order = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        path = config.get('file', None)
        _logger = logging.getLogger(__name__)
        if path:
            level = config.get('level', 'INFO').upper()
            conversor = logging._nameToLevel
            levels = []
            for lev in order:
                levels.append(conversor[lev])
                if lev == level:
                    break

            _logger.setLevel(conversor[level])
            _logger.addHandler(logger.FileLevelHandler(
                filename=path,
                levels=levels,
                backup=config.getint('backup_file_rotation', 5),
                size=config.getint('max_file_size', 20000000)
            ))

        return _logger

    def authorization(self, paymethod, amount, order=None, reconciliation=None,
                      custom_01=None, custom_02=None, tokenize=None):
        """Send a request of authorization to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        payload = {
            'order': order,
            'reconciliation': reconciliation,
            'custom_01': custom_01,
            'custom_02': custom_02,
            'amount': amount.amount,
            'currency': amount.currency
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        paymethod.add_to(payload)

        if tokenize is not None and not re.match(r'^[\w-]{6,128}$', tokenize):
            self._logger.error('Value of tokenize is incorrect.')
            raise ValueError('Value of tokenize is incorrect.')

        if 'token' not in payload and tokenize is not None:
            payload['token'] = tokenize

        response = self.send(payload, 'authorization')
        return Operation(response) if response else None

    def refund(self, refund_id, amount, order=None, reconciliation=None,
               custom_01=None, custom_02=None, tokenize=None):
        """Send a request of refund to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        payload = {
            'order': order,
            'reconciliation': reconciliation,
            'custom_01': custom_01,
            'custom_02': custom_02,
            'amount': amount.amount,
            'currency': amount.currency
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        if isinstance(refund_id, str):
            payload['transaction_id'] = refund_id
        elif issubclass(type(refund_id), PayMethod):
            refund_id.add_to(payload)
        else:
            self._logger.error('Incorrect refund_id.')
            raise TypeError('Incorrect refund_id.')

        if tokenize is not None and not re.match(r'^[\w-]{6,128}$', tokenize):
            self._logger.error('Value of tokenize is incorrect.')
            raise ValueError('Value of tokenize is incorrect.')

        if 'token' not in payload and tokenize is not None:
            payload['token'] = tokenize

        response = self.send(payload, 'refund')
        return Operation(response) if response else None

    def register(self, card_pan, token):
        """Send a request of register to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        if not isinstance(token, str) or \
           not re.match(r'^[\w-]{6,128}$', token):
            self._logger.error('Value of token is incorrect.')
            raise ValueError('Value of token is incorrect.')

        payload = {
            'token': token
        }
        if isinstance(card_pan.card_id, tuple):
            card_pan.add_to(payload)
        else:
            self._logger.error('Incorrect card_pan.')
            raise TypeError('Incorrect card_pan.')

        return MaskedCard(self.send(payload, 'register'))

    def card(self, token):
        """Send a request of save a card to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        if not isinstance(token, str) or \
           not re.match(r'^[\w-]{6,128}$', token):
            self._logger.error('Value of token is incorrect.')
            raise ValueError('Value of token is incorrect.')

        payload = {
            'token': token
        }

        response = self.send(payload, 'card')
        return MaskedCard(response) if response else None

    def cancellation(self, transaction_id):
        """Send a request of cancellation to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        if not isinstance(transaction_id, str) or \
           not re.match(r'^[0-9]{6,22}$', transaction_id):
            self._logger.error('Value of transaction_id is incorrect.')
            raise ValueError('Value of transaction_id is incorrect.')

        payload = {
            'transaction_id': transaction_id
        }

        response = self.send(payload, 'cancellation')
        return Confirmation(response) if response else None

    def unregister(self, token):
        """Send a request of remove a registry of a token to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        if not isinstance(token, str) or \
           not re.match(r'^[\w-]{6,128}$', token):
            self._logger.error('Value of token is incorrect.')
            raise ValueError('Value of token is incorrect.')

        payload = {
            'token': token
        }

        response = self.send(payload, 'unregister')
        return Confirmation(response) if response else None

    def query(self, order=None, transaction_id=None):
        """Send a query to Sipay."""
        # IDEA: Poner schema al pricipio de cada funcion que capture los
        # errores y utilizar logger para reportar error
        payload = {
            'order': order,
            'transaction_id': transaction_id
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        response = self.send(payload, 'query')
        return Query(response) if response else None
