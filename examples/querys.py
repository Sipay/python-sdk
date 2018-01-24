"""Query example."""

from sipay import Ecommerce

ecommerce = Ecommerce('etc/config.ini')

# Consultar tarjeta
card_res = ecommerce.card('tokenCard')

if card_res.code < 0:
    print('Fallo al consultar la tarjeta, Error: {}'.format(card_res.description))

elif card_res.code == 0:
    print('Consulta procesada correctamente')

else:
    print('Consulta procesada correctamente, Warning: {}'.format(card_res.description))

# card_res.card devuelve la tarjeta StoredCard

# Consultar operación por id
query = ecommerce.query(transaction_id='transaction_id')

if query.code < 0:
    print('Fallo al hacer la consulta, Error: {}'.format(query.description))

elif query.code == 0:
    print('Consulta procesada correctamente')

    for transaction in query.transactions:
        print(transaction)

else:
    print('Consulta procesada correctamente, Warning: {}'.format(query.description))

# Consultar operación por ticket
query2 = ecommerce.query(order='order')

if query2.code < 0:
    print('Fallo al hacer la consulta, Error: {}'.format(query2.description))

elif query2.code == 0:
    print('Consulta procesada correctamente')

    for transaction in query.transactions:
        print(transaction)

else:
    print('Consulta procesada correctamente, Warning: {}'.format(query2.description))
