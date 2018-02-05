"""Ecommerce module."""
from configparser import ConfigParser
from time import time
import hmac
import json
import requests
import logging

from sipay.ecommerce.responses.authorization import Authorization
from sipay.ecommerce.responses.cancellation import Cancellation
from sipay.ecommerce.responses.card import Card as CardResponse
from sipay.ecommerce.responses.refund import Refund
from sipay.ecommerce.responses.register import Register
from sipay.ecommerce.responses.unregister import Unregister
from sipay.ecommerce.responses.query import Query
from sipay.paymethod import PayMethod
from sipay.paymethod.card import Card
from sipay.amount import Amount

from sipay.utils import schema

from sipay.logger import FileLevelHandler


class Ecommerce:
    """SDK to use middleware of Sipay easily."""

    def __init__(self, config_file):
        """Initialize Ecommerce with a config.ini file."""
        if not isinstance(config_file, str):
            self._logger.error('config_file must be a string.')
            raise TypeError('config_file must be a string.')

        config = ConfigParser()
        config.read(config_file)

        self._logger = self._get_logger(config['logger'])

        cred = config['credentials']
        self.key = cred.get('key', '')
        self.secret = cred.get('secret', '')
        self.resource = cred.get('resource', '')

        api = config['api']
        self.environment = api.get('environment', '')
        self.version = api.get('version', '')
        self.mode = api.get('mode', '')

        timeout = config['timeout']
        self.conn_timeout = timeout.getint('connection', 3)
        self.process_timeout = timeout.getint('process', 27)

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
    def environment(self):
        """Getter of environment."""
        return self._environment

    @environment.setter
    def environment(self, environment):
        if not isinstance(environment, str):
            self._logger.error('environment must be a string.')
            raise TypeError('environment must be a string.')

        environment = environment.lower()
        if environment not in ['sandbox', 'staging', 'live']:
            self._logger.error('environment must be sandbox, staging or live')
            raise ValueError('environment must be sandbox, staging or live')

        self._environment = environment

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
    def conn_timeout(self):
        """Getter of conn_timeout."""
        return self._conn_timeout

    @conn_timeout.setter
    def conn_timeout(self, conn_timeout):
        if not isinstance(conn_timeout, int):
            self._logger.error('conn_timeout must be an integer.')
            raise TypeError('conn_timeout must be an integer.')

        if conn_timeout <= 0:
            self._logger.error('conn_timeout must be geater than 0.')
            raise ValueError('conn_timeout must be geater than 0.')

        self._conn_timeout = conn_timeout

    @property
    def process_timeout(self):
        """Getter of process_timeout."""
        return self._process_timeout

    @process_timeout.setter
    def process_timeout(self, process_timeout):
        if not isinstance(process_timeout, int):
            self._logger.error('process_timeout must be an integer.')
            raise TypeError('process_timeout must be an integer.')

        if process_timeout <= 0:
            self._logger.error('process_timeout must be geater than 0.')
            raise ValueError('process_timeout must be geater than 0.')

        self._process_timeout = process_timeout

    def send(self, payload, endpoint):
        """Send payload to endpoint."""
        self._logger.info('Start send to endpoint ' + endpoint)
        nonce = str(time()).replace('.', '')
        secret = bytes(self.secret, 'utf-8')
        params = {
          'key': self.key,
          'resource': self.resource,
          'nonce': nonce,
          'mode': self.mode,
          'payload': payload
        }
        body = json.dumps(params)

        sign = hmac.new(secret, bytes(body, 'utf-8'), self.mode).hexdigest()
        headers = {
            'Content-Type': 'application/json',
            'Content-Signature': sign
        }
        url = 'https://{0}.sipay.es/mdwr/{1}/{2}'.format(self.environment,
                                                         self.version,
                                                         endpoint)

        try:
            r = requests.post(url, headers=headers, data=body,
                              timeout=(self.conn_timeout,
                                       self.process_timeout))
            response = r.json()
            request = r.request.__dict__

        except Exception:
            self._logger.exception('Exception in post')
            response = None
            request = {
                'url': url,
                'body': params,
                'header': headers
            }

        self._logger.info('End send to endpoint ' + endpoint)

        return (request, response)

    def _get_logger(self, config):
        """Set global logger."""
        order = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        path = config.get('file', None)
        _logger = logging.getLogger(__name__)
        if path:
            level = config.get('level', 'INFO').upper()
            if level not in order:
                Exception('Incorrect levels.')

            _logger.setLevel(getattr(logging, level))
            _logger.addHandler(FileLevelHandler(
                filename=path,
                backup=config.getint('backup_file_rotation', 5),
                size=config.getint('max_file_size', 20000000)
            ))

        return _logger

    @schema({
        'amount': {'type': Amount},
        'order': {'type': str, 'pattern': r'^[\w-]{6,64}$'},
        'reconciliation': {
            'type': str,
            'pattern': r'^[0-9]{4}[a-zA-Z0-9]{0,8}$'},
        'custom_01': {'type': str},
        'custom_02': {'type': str},
        'token': {'type': str, 'pattern': r'^[\w-]{6,128}$'}
        })
    def authorization(self, paymethod, amount, order=None, reconciliation=None,
                      custom_01=None, custom_02=None, token=None):
        """Send a request of authorization to Sipay.

        Args:
            - paymethod: Payment method of authorization (it can be an object
                of Card, StoredCard or FastPay).
            - amount: Amount of the operation.
            - order: ticket of the operation
            - reconciliation: identification for bank reconciliation
            - custom_01: custom field 1
            - custom_02: custom field 2
            - token: if this argument is set, it register paymethod with
                this token
        Return:
            Authorization: object that contain response of MDWR API
        """
        if not issubclass(type(paymethod), PayMethod):
            TypeError("paymethod isn't a PayMethod")

        payload = {
            'order': order,
            'reconciliation': reconciliation,
            'custom_01': custom_01,
            'custom_02': custom_02,
            'amount': amount.amount,
            'currency': amount.currency
        }

        payload.update(paymethod.to_dict())

        if 'token' not in payload and token is not None:
            payload['token'] = token

        payload = {k: v for k, v in payload.items() if v is not None}

        request, response = self.send(payload, 'authorization')
        return Authorization(request, response) if response else None

    @schema({
        'amount': {'type': Amount},
        'order': {'type': str, 'pattern': r'^[\w-]{6,64}$'},
        'reconciliation': {
            'type': str,
            'pattern': r'^[0-9]{4}[a-zA-Z0-9]{0,8}$'},
        'custom_01': {'type': str},
        'custom_02': {'type': str},
        'token': {'type': str, 'pattern': r'^[\w-]{6,128}$'}
        })
    def refund(self, identificator, amount, order=None, reconciliation=None,
               custom_01=None, custom_02=None, token=None):
        """Send a request of refund to Sipay.

        Args:
            - identificator: identificator of refundation (it can be a
                PayMethod or transaction_id).
            - amount: Amount of the operation.
            - order: ticket of the operation
            - reconciliation: identification for bank reconciliation
            - custom_01: custom field 1
            - custom_02: custom field 2
            - token: if this argument is set, it register paymethod with
                this token
        Return:
            Refund: object that contain response of MDWR API
        """
        payload = {
            'order': order,
            'reconciliation': reconciliation,
            'custom_01': custom_01,
            'custom_02': custom_02,
            'amount': amount.amount,
            'currency': amount.currency
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        if isinstance(identificator, str):
            payload['transaction_id'] = identificator
        elif issubclass(type(identificator), PayMethod):
            payload.update(identificator.to_dict())
        else:
            self._logger.error('Incorrect identificator.')
            raise TypeError('Incorrect identificator.')

        if 'token' not in payload and token is not None:
            payload['token'] = token

        request, response = self.send(payload, 'refund')
        return Refund(request, response) if response else None

    @schema({
        'card': {'type': Card},
        'token': {'type': str, 'pattern': r'^[\w-]{6,128}$'}
        })
    def register(self, card, token):
        """Send a request of register to Sipay.

        Args:
            - card: Card that register.
            - token: token will be associate to card
        Return:
            Register: object that contain response of MDWR API
        """
        payload = {
            'token': token
        }
        payload.update(card.to_dict())

        request, response = self.send(payload, 'register')
        return Register(request, response) if response else None

    @schema({'token': {'type': str, 'pattern': r'^[\w-]{6,128}$'}})
    def card(self, token):
        """Send a request for search a card in Sipay.

        Args:
            - token: token of card
        Return:
            Card(Response): object that contain response of MDWR API
        """
        payload = {
            'token': token
        }

        request, response = self.send(payload, 'card')
        return CardResponse(request, response) if response else None

    @schema({'transaction_id': {'type': str, 'pattern': r'^[0-9]{6,22}$'}})
    def cancellation(self, transaction_id):
        """Send a request of cancellation to Sipay.

        Args:
            - transaction_id: identificator of transaction.
        Return:
            Cancellation(Response): object that contain response of MDWR API
        """
        payload = {
            'transaction_id': transaction_id
        }

        request, response = self.send(payload, 'cancellation')
        return Cancellation(request, response) if response else None

    @schema({'token': {'type': str, 'pattern': r'^[\w-]{6,128}$'}})
    def unregister(self, token):
        """Send a request of remove a registry of a token to Sipay.

        Args:
            - token: token of a card
        Return:
            Unregister: object that contain response of MDWR API
        """
        payload = {
            'token': token
        }

        request, response = self.send(payload, 'unregister')
        return Unregister(request, response) if response else None

    @schema({
        'order': {'type': str, 'pattern': r'^[\w-]{6,64}$'},
        'transaction_id': {'type': str, 'pattern': r'^[0-9]{6,22}$'}
        })
    def query(self, order=None, transaction_id=None):
        """Send a query to Sipay.

        Args:
            - order: ticket of the operation
            - transaction_id: identificator of transaction
        Return:
            Query: object that contain response of MDWR API
        """
        payload = {
            'order': order,
            'transaction_id': transaction_id
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        request, response = self.send(payload, 'query')
        return Query(request, response) if response else None
