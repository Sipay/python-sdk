"""Methods module."""
from sipay.altp.responses import Response


class Methods(Response):
    """Methods class."""
    def __init__(self, request, response):
        """Initialize."""
        super().__init__(request, response)
        if response.get('payload'):
            payload = response['payload']
            methods = payload['methods']
            pexp = methods.get('paypal_express_checkout')
            pref = methods.get('paypal_reference_transaction')
            sfrt = methods.get('sofort')
            pmt = methods.get('pmt')
            movi = methods.get('movistar_identify')
            self.movi = None

            methods = {
                'pexp': pexp.get('url'),
                'pref': pref.get('url'),
                'pmt': pmt.get('url'),
                'sfrt': sfrt.get('url'),
                'movi': None
            }
            if movi is not None:
                method_to_add = {'movi': movi.get('url')}
                methods.update(method_to_add)
                self.movi = movi.get('url')

            self.pexp = pexp.get('url')
            self.pref = pref.get('url')
            self.pmt = pmt.get('url')
            self.sfrt = sfrt.get('url')
            self.methods = methods
