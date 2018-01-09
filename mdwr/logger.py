"""Utils for logging."""
import logging
import logging.handlers

LOGFMT = '{asctime} {levelname:>8} - {name}({lineno}): {message}'
FORMATTER = logging.Formatter(fmt=LOGFMT, style='{')

PAN_KEYS = {'pan', 'card_number', 'Ds_Cardholder_Pan'}
HIDDEN_KEYS = {'cvv', 'password'}


class FileLevelHandler(logging.handlers.RotatingFileHandler):
    """File handler."""

    def __init__(self, filename, size=0, backup=0, fmt=FORMATTER):
        """Initialize handler."""
        super().__init__(filename, maxBytes=size, backupCount=backup)
        self.setFormatter(fmt)


class Logger(logging.LoggerAdapter):
    """Logger adapter."""

    def process(self, msg, kwargs):
        """Process log."""
        extra = dict(self.extra, **kwargs.pop('extra', {}))

        params = [('uuid', extra.pop('uuid', '')), ('msg', msg)]

        params.extend(extra.items())

        msg = ' '.join('{}={};'.format(k, v) for k, v in self.parse(params))

        return msg, kwargs

    def parse(self, params, data=None, keys=None):
        """Parse extra data logs."""
        data = data or []
        keys = keys or []

        for key, value in params:
            if isinstance(value, dict):
                self.parse(value.items(), data, keys + [key])

            elif isinstance(value, (list, set)):
                self.parse(enumerate(value), data, keys + [key])

            else:
                ns = list(map(str, keys + [key]))

                if value is None:
                    value = ''

                elif HIDDEN_KEYS & set(ns):
                    value = '*' * len(str(value))

                elif PAN_KEYS & set(ns):
                    value = '{}******{}'.format(value[:6], value[-4:])

                data.append(('.'.join(ns), value))

        return data
