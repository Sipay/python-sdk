"""Ecommerce module."""
from configparser import ConfigParser
from time import time
import hmac
import json
import requests
import logging
import pprint


from sipay.amount import Amount
from sipay.altp.responses.methods import Methods
from sipay.altp.responses.status import Status
from sipay.altp.responses.confirm import Confirm
from sipay.altp.responses.payment import Payment
from sipay.altp.responses.purchase_from_token import Purchase_from_token


from sipay.utils import schema

from sipay.logger import FileLevelHandler


class Altp:
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
        nonce = (str(time()).replace('.', ''))[-10:]
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
        # url = 'https://{0}.sipay.es/altp/{1}/{2}'.format(self.environment,
        #                                                 self.version,
        #                                                 endpoint)

        url = 'https://develop.sipay.es/altp/{0}/{1}'.format(self.version, endpoint)  # noqa
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
        'result': {'type': str},
        'amount': {'type': Amount},
        })
    def methods(self, result, amount, **kwargs):

        payload = {
            'currency': amount.currency,
            'amount': amount.amount,
            'notify': {
                'result': result
            },
            'policy_data': {}
        }

        if kwargs.get('description'):
            payload_to_add = {
                'billing': {
                    'description': kwargs['description']
                }
            }
            payload.update(payload_to_add)

        if kwargs.get('email') and kwargs.get('full_name'):
            payload_to_add = {
                'customer': {
                    'email': kwargs['email'],
                    'full_name': kwargs['full_name']
                }
            }
            payload.update(payload_to_add)

        if kwargs.get('msisdn'):
            payload_to_add = {
                'msisdn': '34611111111'
            }
            payload.update(payload_to_add)

        request, response = self.send(payload, 'methods')
        return Methods(request, response) if response else None

    @schema({
        'request_id': {'type': str}
        })
    def status(self, request_id):

        payload = {
            'request_id': request_id
        }

        request, response = self.send(payload, 'status/operation')
        return Status(request, response) if response else None

    @schema({
        'request_id': {'type': str},
        'payment_type': {'type': str}
        })
    def confirm(self, request_id, payment_type, **kwargs):

        payload = {
            'request_id': request_id
        }

        if kwargs.get('opt'):
            payload_to_add = {
                'opt': kwargs['opt']
            }
            payload.update(payload_to_add)

        request, response = self.send(payload, '{0}/confirm'.format(payment_type))  # noqa
        return Confirm(request, response) if response else None

    @schema({
        'amount': {'type': str},
        'currency': {'type': str},
        'billing_id': {'type': str},
        'order': {'type': str},
        })
    def payment(self, amount, currency, billing_id, order, reconciliation=None):  # noqa

        payload = {
            'amount': amount,
            'currency': currency,
            'billing_id': billing_id,
            'order': order,
            'reconciliation': reconciliation
        }

        request, response = self.send(payload, 'pref/payment')
        return Payment(request, response) if response else None

    @schema({
        'amount': {'type': str},
        'currency': {'type': str},
        'auth_token': {'type': str},
        'client_ip_address': {'type': str},
        })
    def purchase_from_token(self, amount, currency, auth_token, client_ip_address,  # noqa
                                order=None, notes=None, pe_notification_url=None,  # noqa
                                channel=None, custom_params=None, language=None, message_params=None):  # noqa

        payload = {
            'amount': amount,
            'currency': currency,
            'auth_token': auth_token,
            'client_ip_address': client_ip_address,
            'order': order,
            'notes': notes,
            'pe_notification_url': pe_notification_url,
            'channel': channel,
            'custom_params': custom_params,
            'language': language,
            'message_params': message_params
        }

        pprint.pprint(payload)
        request, response = self.send(payload, 'movi/purchase_from_token')
        return Purchase_from_token(request, response) if response else None
