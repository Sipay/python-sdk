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
card = Card(pan_example, 2020, 2)
# card = StoredCard('token')
# card = FastPay('token')

refund2 = ecommerce.refund(card, amount)

if not refund2:
    print('Fallo al hacer la devolución, Error al conectar con el servicio')

elif refund2.code != 0:
    print('Fallo al hacer la devolución, Error: {}'.format(refund2.description))  # noqa

else:
    print('Devolución procesada correctamente')

# Almacenar tarjeta en Sipay
card = Card(pan_example, 2020, 2)
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


# Realizar una preautorización de 8.34 euros con Sipay
amount = Amount(834, 'EUR')
card = Card(pan_example, 2020, 2)

preauth = ecommerce.preauthorization(card, amount)

if not preauth:
elif preauth.code != 0:
    print('Fallo al realizar la preautorización, Error: {}'.format(preauth.description)) # noqa
elif preauth.code != 0:
    print('Fallo al realizar la preautorización, Error: {}'.format(preauth.description))  # noqa

else:
    print('Preautorización creada correctamente')


# Realizar un desbloqueo de una preautorización de 8.34 
# euros útilizando una instancia de preautorización 

unlock = ecommerce.unlock(preauth, amount)

if not unlock:
    print('Fallo al hacer realizar el desbloqueo de la preautorización, Error al conectar con el servicio') # noqa

elif unlock.code != 0:
    print('Fallo al realizar el desbloqueo de la preautorización, Error: {}'.format(unlock.description)) # noqa

else:
    print('Desbloqueo de preautorización realizado con exito')

# Realizar un desbloqueo de una preautorización de 8.34 euros útilizando un transaction_id  # noqa

unlock2 = ecommerce.unlock('000097586585926825335', amount)
# El transaction_id se obtiene al haber realizado una preautorización

if not unlock2:
    print('Fallo al hacer realizar el desbloqueo de la preautorización, Error al conectar con el servicio') # noqa

elif unlock2.code != 0:
    print('Fallo al realizar el desbloqueo de la preautorización, Error: {}'.format(unlock2.description))  # noqa

else:
    print('Desbloqueo de preautorización realizado con exito')

# Realizar una confirmación de una preautorización de 8.34 euros útilizando una instancia de preautorización  # noqa

confirm = ecommerce.confirmation(preauth, amount)

if not confirm:
    print('Fallo al hacer realizar la confirmación de la preautorización, Error al conectar con el servicio')  # noqa

elif confirm.code != 0:
    print('Fallo al realizar la confirmación de la preautorización, Error: {}'.format(confirm.description))  # noqa
else:
    print('Confirmación de preautorización realizada con exito')

# Realizar un desbloqueo de una preautorización útilizando un transaction_id

confirm2 = ecommerce.confirmation('000097586585926825335', amount)

# El transaction_id se obtiene al haber realizado una preautorización

if not confirm2:
    print('Fallo al hacer realizar la confirmación de la preautorización, Error al conectar con el servicio')  # noqa
elif confirm2.code != 0:
    print('Fallo al realizar la confirmación de la preautorización, Error: {}'.format(confirm2.description))  # noqa

else:
    print('Confirmación de preautorización realizado con exito')
