"""Operations script."""
from sipay import Ecommerce
from sipay.paymethod.card import Card
from sipay.paymethod.storedcard import StoredCard
from sipay.paymethod.fastpay import FastPay
from sipay.amount import Amount

from pathlib import Path

parent = str(Path(__file__).parent.resolve().parent)
config_file = '{}/etc/config.ini'.format(parent)

ecommerce = Ecommerce(config_file)

# pago de un Euro con tarjeta y almacenar en Sipay con un token
pan_example = '4242424242424242'

amount = Amount(100, 'EUR')
card = Card(pan_example, 2050, 2)
token = '2977e78d1e3e4c9fa6b70'

auth = ecommerce.authorization(card, amount, token=token)
if not auth:
    print('Fallo al realizar el pago, Error al conectar con el servicio')

elif auth.code != 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth.description))

else:
    print('Pago procesado correctamente')


# pago de 4.56 euros con tarjeta ya almacenada en Sipay
amount = Amount(456, 'EUR')
token = '2977e78d1e3e4c9fa6b70'
card = StoredCard(token)


auth2 = ecommerce.authorization(card, amount)

if not auth2:
    print('Fallo al realizar el pago, Error al conectar con el servicio')

elif auth2.code != 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth2.description))

else:
    print('Pago procesado correctamente')

# pago de 2.34 euros con tarjeta ya almacenada en Sipay mediante FastPay
amount = Amount('2.34', 'EUR')
token_fastpay = '2977e78d1e3e4c9fa6b70ab294ef3ee4'
card = FastPay(token_fastpay)

auth3 = ecommerce.authorization(card, amount)

if not auth3:
    print('Fallo al realizar el pago, Error al conectar con el servicio')

elif auth3.code != 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth3.description))

else:
    print('Pago procesado correctamente')

# cancelar el pago con tarjeta (auth)
cancel = ecommerce.cancellation(auth.transaction_id)
if not cancel:
    print('Fallo al cancelar el pago, Error al conectar con el servicio')

elif cancel.code != 0:
    print('Fallo al cancelar el pago, Error: {}'.format(cancel.description))

else:
    print('Cancelación procesada correctamente')

# Hacer una devolución con identificador de transacción de 8.34 euros
amount = Amount(834, 'EUR')

refund = ecommerce.refund(auth2.transaction_id, amount)
if not refund:
    print('Fallo al hacer la devolución, Error al conectar con el servicio')

elif refund.code != 0:
    print('Fallo al hacer la devolución, Error: {}'.format(refund.description))

else:
    print('Devolución procesada correctamente')

# Hacer una devolución con tarjeta de 28.60 euros
amount = Amount(2860, 'EUR')
card = Card(pan_example, 2018, 2)
# card = StoredCard('token')
# card = FastPay('token')

refund2 = ecommerce.refund(card, amount)

if not refund2:
    print('Fallo al hacer la devolución, Error al conectar con el servicio')

elif refund2.code != 0:
    print('Fallo al hacer la devolución, Error: {}'.format(refund2.description))  # noqa

else:
    print('Devolución procesada correctamente')

# Al macenar tarjeta en Sipay
card = Card(pan_example, 2018, 2)
# card = FastPay('token')

register = ecommerce.register(card, 'newtoken')

if not register:
    print('Fallo al registrar la tarjeta, Error al conectar con el servicio')

elif register.code != 0:
    print('Fallo al registrar la tarjeta, Error: {}'.format(register.description))  # noqa

else:
    print('Registro procesado correctamente')

# register.card devuelve la tarjeta StoredCard

# Borrar tarjeta de Sipay
unregister = ecommerce.unregister('newtoken')

if not unregister:
    print('Fallo al borrar la tarjeta de Sipay, Error al conectar con el servicio')  # noqa

elif unregister.code != 0:
    print('Fallo al borrar la tarjeta de Sipay, Error: {}'.format(unregister.description))  # noqa

else:
    print('Tarjeta borrada correctamente')
