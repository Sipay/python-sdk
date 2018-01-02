# Instalación

  ```bash
    $ git clone url
  ```

# Documentación

Para utilizar la SDK del middleware, hay que importar el paquete y crear el objeto con la ruta del archivo de configuración.

```python
  from mdwr import MDWR
  mdwr = MDWR('etc/config.ini')
```

El archivo de configuración tiene que
```ini
# **************************************************************
# LOGGER
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configuración asociada al sistema de trazas.
#
# file: Nombre del archivo
# level: nivel minimo de trazas [debug, info, warning, error, critical]
# max_file_size: Tamaño máximo del fichero de trazas [bytes]
# backup_file_rotation: Número de ficheros de backup
# ------------------------------------------------------------//

[logger]
file=logs/info.log
level=warning
max_file_size = 51200000
backup_file_rotation = 5

# **************************************************************
# CREDENTIALS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Credenciales para obtener acceso al recurso.
#
# key: Key del cliente
# secret: Secret del cliente
# resouce: Recurso al que se quiere acceder
# ------------------------------------------------------------//

[credentials]
key=api-key
secret=api-secret
resource=resource

# **************************************************************
# API
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Configuracion de la API.
#
# environment: Entorno al que se deben enviar las peticiones ['sandbox', 'staging', 'live']
# version: Versión de la api a usar actualmente solo existe v1
# mode: Modo de encriptacion de la firma, [sha256, sha512]
# ------------------------------------------------------------//

[api]
environment=sandbox
version=v1
mode=sha256

# **************************************************************
# TIMEOUT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Cofiguracion de los tiempos de timeout.
#
# connection: Timeout de connexión en segundos
# process: Timeout de procesamiento en segundos
# ------------------------------------------------------------//

[timeout]
connection=3
process=27
```

Tras iniciar el objeto `mdwr` se puede realizar las siguientes llamadas:
 * **Authorization**

  * **pay_method(PayMethod, required):** metodo de pago [tarjeta, fastpay]
  * **amount(Amount, required):** importe de la operación
  * **order (string):** Ticket de la operación.
  * **reconciliation (string):** Identificador para la conciliación bancaria.
  * **custom_01 (string):** Campo personalizable.
  * **custom_02 (string):** Campo personalizable.
  * **tokenize(string):** Si el método de pago no es una tarjeta tokenizada, y el valor de tokenize es un str no vacío tokeniza la tarjeta asociada

 Ejemplo:

 Autorización con tarjeta.

 ```python
   from mdwr.paymethod.card import Card
   from mdwr.amount import Amount

   amount = Amount(100, 'EUR') # 1€
   card = Card(('6712009000000205', 2018, 2))

   auth = mdwr.authorization(card, amount)
 ```

 Autorización con Fast Pay.

 ```python
   from mdwr.paymethod.fastpay import FastPay
   from mdwr.amount import Amount

   amount = Amount(100, 'EUR') # 1€
   fp = FastPay('830dc0b45f8945fab229000347646ca5')

   auth = mdwr.authorization(fp, amount)
 ```

 authorization devuelve un objeto Operation.

* **Refund**

  * **pay_method(PayMethod):** Método de pago.
  * **amount (Amount, required):** Importe de la operación
  * **transaction_id (string):** Identificador de la transacción.
  * **order (string):** Ticket de la operación.
  * **reconciliation (string):** Identificador para la conciliación bancaria.
  * **custom_01 (string):** Campo personalizable.
  * **custom_02 (string):** Campo personalizable.
  * **tokenize(string):** Si el método de pago no es una tarjeta tokenizada, y el valor de tokenize es un str no vacío tokeniza la tarjeta asociada

  El método de pago o el identificador de la transacción es requerido.

  Ejemplo:

  Devolución con tarjeta.

  ```python
    from mdwr.paymethod.card import Card
    from mdwr.amount import Amount

    amount = Amount(100, 'EUR') # 1€
    card = Card('bd6613acc6bd4ac7b6aa96fb92b2572a')

    refund = mdwr.refund(card, amount)
  ```

  Devolución con transaction_id.

  ```python
    from mdwr.amount import Amount

    amount = Amount(100, 'EUR') # 1€

    refund = mdwr.refund('transaction_id', amount)
  ```

  refund devuelve un objeto Operation.

  * **Register**

    * **card(Card):** Tarjeta iniciada con `(pan, año, mes)`.
    * **tokenize(string):** Token con el que se le asocia a la tarjeta.

    Ejemplo:

    Registro de tarjeta.

    ```python
      from mdwr.paymethod.card import Card

      card = Card(('6712009000000205', 2018, 2))

      masked_card = mdwr.register(card, 'newtoken')
    ```

    register devuelve un objeto MaskedCard.

    refund devuelve un objeto Operation.

* **Card**

  * **token(string):** Token asociado a la tarjeta.

  Ejemplo:

  Búsqueda de tarjeta.

  ```python
    masked_card = mdwr.card('newtoken')
  ```

  card devuelve un objeto MaskedCard.
