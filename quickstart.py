"""Quick Start script."""
from sipay import Ecommerce
from sipay.paymethod.card import Card
from sipay.paymethod.storedcard import StoredCard
from sipay.paymethod.fastpay import FastPay
from sipay.amount import Amount

ecommerce = Ecommerce('etc/config.ini')

# pago de un Euro con tarjeta y almacenar en Sipay con un token
amount = Amount(100, 'EUR')
card = Card('6712009000000205', 2018, 2)
token = '2977e78d1e3e4c9fa6b70'

auth = ecommerce.authorization(card, amount, token=token)

if auth.code < 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth.description))

elif auth.code == 0:
    print('Pago procesado correctamente')

else:
    print('Pago procesado correctamente, Warning: {}'.format(auth.description))

# pago de 4.56 euros con tarjeta ya almacenada en Sipay
amount = Amount(456, 'EUR')
token = '2977e78d1e3e4c9fa6b70'
card = StoredCard(token)


auth2 = ecommerce.authorization(card, amount)

if auth2.code < 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth2.description))

elif auth2.code == 0:
    print('Pago procesado correctamente')

else:
    print('Pago procesado correctamente, Warning: {}'.format(auth2.description))

# pago de 2.34 euros con tarjeta ya almacenada en Sipay mediante FastPay
amount = Amount('2.34', 'EUR')
token_fastpay = '2977e78d1e3e4c9fa6b70ab294ef3ee4'
card = FastPay(token_fastpay)

auth3 = ecommerce.authorization(card, amount)

if auth3.code < 0:
    print('Fallo al realizar el pago, Error: {}'.format(auth3.description))

elif auth3.code == 0:
    print('Pago procesado correctamente')

else:
    print('Pago procesado correctamente, Warning: {}'.format(auth3.description))

# cancelar le pago con tarjeta (auth)
cancel = ecommerce.cancellation(auth.transaction_id)
if cancel.code < 0:
    print('Fallo al cancelar el pago, Error: {}'.format(cancel.description))

elif cancel.code == 0:
    print('Cancelación procesada correctamente')

else:
    print('Cancelación procesada correctamente, Warning: {}'.format(cancel.description))

# Hacer una devolución con identificador de transacción de 8.34 euros
amount = Amount(834, 'EUR')

refund = ecommerce.refund(auth2.transaction_id, amount)
if refund.code < 0:
    print('Fallo al hacer la devolución, Error: {}'.format(refund.description))

elif refund.code == 0:
    print('Devolución procesada correctamente')

else:
    print('Devolución procesada correctamente, Warning: {}'.format(refund.description))

# Hacer una devolución con tarjeta de 28.60 euros
amount = Amount(2860, 'EUR')
card = Card('6712009000000205', 2018, 2)
# card = StoredCard('token')
# card = FastPay('token')

refund2 = ecommerce.refund(card, amount)

if refund2.code < 0:
    print('Fallo al hacer la devolución, Error: {}'.format(refund2.description))

elif refund2.code == 0:
    print('Devolución procesada correctamente')

else:
    print('Devolución procesada correctamente, Warning: {}'.format(refund2.description))

# Al macenar tarjeta en Sipay
card = Card('6712009000000205', 2018, 2)
# card = FastPay('token')

register = ecommerce.register(card, 'newtoken')

if register.code < 0:
    print('Fallo al registrar la tarjeta, Error: {}'.format(register.description))

elif register.code == 0:
    print('Registro procesado correctamente')

else:
    print('Registro procesado correctamente, Warning: {}'.format(register.description))

# register.card devuelve la tarjeta StoredCard

# Consultar tarjeta
card_res = ecommerce.card('newtoken')

if card_res.code < 0:
    print('Fallo al consultar la tarjeta, Error: {}'.format(card_res.description))

elif card_res.code == 0:
    print('Consulta procesada correctamente')

else:
    print('Consulta procesada correctamente, Warning: {}'.format(card_res.description))

# card_res.card devuelve la tarjeta StoredCard

# Borrar tarjeta de Sipay
unregister = ecommerce.unregister('newtoken')

if unregister.code < 0:
    print('Fallo al borrar la tarjeta de Sipay, Error: {}'.format(unregister.description))

elif unregister.code == 0:
    print('Tarjeta borrada correctamente')

else:
    print('Tarjeta borrada correctamente, Warning: {}'.format(unregister.description))

# Consultar operación
query = ecommerce.query(auth2.transaction_id)

if query.code < 0:
    print('Fallo al hacer la consulta, Error: {}'.format(query.description))

elif query.code == 0:
    print('Consulta procesada correctamente')

    for transaction in query.transactions:
        print(transaction)

else:
    print('Consulta procesada correctamente, Warning: {}'.format(query.description))
