"""Transaction module."""
from sipay.amount import Amount
from datetime import datetime


class Transaction:
    """Transaction class."""

    def __init__(self, data):
        """Initialize."""
        self.channel_name = data['channel_name']
        self.channel = data['channel']
        self.method = data['method']
        self.date = datetime.strptime(data['date'] + data['time'],
                                      '%Y-%m-%d%H:%M:%S')
        self.order = data['order']
        self.transaction_id = data['transaction_id']
        self.internal_code = data['code']
        self.method_name = data['method_name']
        self.operation = data['operation']
        self.amount = Amount(int(data['amount']), data['currency'])
        self.authorization_id = data['authorization_id']
        self.description = data['description']
        self.masked_card = data['masked_card']
        self.operation_name = data['operation_name']
        self.status = data['status']

    def __str__(self):
        """Cast to string."""
        ret = ''
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                ret += '{0}={1}, '.format(k, v)

        ret = '<{0}({1})>'.format(type(self).__name__,ret[:-2])

        return ret
