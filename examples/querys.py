"""Query example."""
from sipay import Ecommerce

from pathlib import Path

parent = str(Path(__file__).parent.resolve().parent)
config_file = '{}/etc/config.ini'.format(parent)

ecommerce = Ecommerce(config_file)

# Consultar tarjeta
card_res = ecommerce.card('tokenCard')

if not card_res:
    print('Fallo al consultar la tarjeta, Error al conectar con el servicio')

elif card_res.code != 0:
    print('Fallo al consultar la tarjeta, Error: {}'.format(card_res.description))  # noqa

else:
    print('Consulta procesada correctamente')

# card_res.card devuelve la tarjeta StoredCard

# Consultar operación por id
query = ecommerce.query(transaction_id='transaction_id')

if not query:
    print('Fallo al hacer la consulta, Error al conectar con el servicio')

elif query.code != 0:
    print('Fallo al hacer la consulta, Error: {}'.format(query.description))

else:
    print('Consulta procesada correctamente')

    for transaction in query.transactions:
        print(transaction)

# Consultar operación por ticket
query2 = ecommerce.query(order='order')

if not query2:
    print('Fallo al hacer la consulta, Error al conectar con el servicio')

elif query2.code != 0:
    print('Fallo al hacer la consulta, Error: {}'.format(query2.description))

elif query2.code == 0:
    print('Consulta procesada correctamente')

    for transaction in query.transactions:
        print(transaction)
