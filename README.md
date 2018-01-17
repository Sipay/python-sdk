# Instalación

  ```bash
    $ git clone url
  ```

# Documentación

## **Objetos**

* **Amount:**

  Este objeto representa una cantidad monetaria, por tanto esta cantidad no puede ser menor igual a 0. Para iniciar un objeto de este tipo se necesita una cantidad y una moneda (código ISO4217)

  La cantidad se puede especificar de dos formas o con un string con la cantidad estandarizada y con el caracter de separación de decimales `.`, o con un entero de la cantidad en la unidad básica e indivisible de la moneda (por ejemplo de la moneda Euro sería el céntimo).

  **Atributos**
    * **amount:** Contiene un entero de la cantidad en la unidad básica e indivisible de la moneda(en el caso de haber introducido un string con decimales, en este campo se almacenará el entero en la unidad básica e indivisible de la moneda).
    * **currency:** Contiene un string del código de la moneda(ISO4217).

  Ejemplos:

  ```python
    from sipay.amount import Amount

    # Con string
    amount = Amount('1.56', 'EUR')

    print(amount)
    # Imprime 1.56EUR
    print(amount.amount)
    # Imprime 156
    print(amount.currency)
    # Imprime EUR

    # Con unidad indivisible
    amount = Amount(156, 'EUR')

    print(amount)
    # Imprime 1.56EUR
    print(amount.amount)
    # Imprime 156
    print(amount.currency)
    # Imprime EUR
  ```
  **Nota:** En el caso de iniciarlo con el string es imprescindible que tenga el número de decimales que indica el estándar ISO4217

### PayMethods

  * **Card:**
    Representa el método de pago con tarjeta, para inicializarlo se necesita:

      * **número de tarjeta:** String que tiene entre 14 y 19 números.
      * **año de caducidad:** Entero de 4 digitos mayor que 2017.
      * **mes de caducidad:** Entero de 2 digitos entre 1 y 12.

    Ejemplo:
    ```python
      from sipay.paymethod.card import Card

      card = Card('0000000000000000', 2018, 2)
    ```


  * **StoredCard:**
  Representa el método de pago con tarjeta almacenada en Sipay, para inicializarlo se necesita:

    * **token asociado a una tarjeta:** String que tiene entre 6 y 128 caracteres alfanúmericos y guiones.

  Ejemplo:
  ```python
    from sipay.paymethod.storedcard import StoredCard

    card = StoredCard('token-card')
  ```
  * **FastPay:**
  Representa el método de pago con tarjeta almacenada en Sipay mediante Fast Pay, para inicializarlo se necesita:

    * **token asociado a una tarjeta:** String que tiene entre 6 y 128 caracteres alfanúmericos y guiones.

  Ejemplo:
  ```python
    from sipay.paymethod.fastpay import FastPay

    fp = FastPay('token-fast-pay')
  ```

### Responses

Todos los objetos de esta sección tienen los siguientes atributos:
- **Atributos comunes:**
  - **type (enum[string]):** Tipo de respuesta:
    * success
    * warning
    * error
  - **code (string):** Código identificador del resultado. Es un código orientativo y no está ligado estrictamente con motivo de la respuesta, es decir, el código no identifica univocamente la respuesta.
    - 0 -> success
    - mayor a 0 -> warning
    - menor a 0 -> error
  - **detail (string):** Código alfanumérico separado con guiones bajos y sin mayúsculas que identifica univocamente la respuesta. Útil para la gestión de los diferentes casos de uso de una operación.
  - **description (string):** Descripción literal del mensaje de respuesta.
  - **uuid (string):** Identificador único de la petición, imprescindible para la trazabilidad.
  - **request_id (string):** Necesario para la finalización de algunas operaciones. Se indicarán aquellas en las que sea necesario.
  - **_request(dictionary):** Son los datos de la petición que se ha hecho al servidor.
  - **_response(dictionary):** Son los datos 'raw' de respuesta.


* **Authorization:**

  Este objeto añade lo atributos:
  * **amount (Amount):** Importe de la operación.
  * **order (string):** Ticket de la operación.
  * **card_trade (string):** Emisor de la tarjeta. Solicite más información.
  * **card_type (string):** Tipo de la tarjeta. Solicite más información.
  * **masked_card (string):** Número de la tarjeta enmascarado.
  * **reconciliation (string):** Identificador para la conciliación bancaria (p37).
  * **transaction_id (string):** Identificador de la transacción.
  * **aproval (string):** Código de aprobación de la entidad.
  * **authorizator (string):** Entidad autorizadora de la operación.


* **Cancellation:**

  Este objeto no añade nada a los atributos anteriores.

* **Card:**

  * **card_mask (string):** Número de la tarjeta enmascarado
  * **expired_at (date):** Fecha de la expiración
  * **token (string):** Identificador de la tarjeta
  * **card(StoredCard):** Objeto tarjeta asociado a la tarjeta devuelta.


* **Query:**

  Este objeto añade una lista de objetos transacciones, cada objeto transacción tiene:

  **Transaction:**
    * **description (string):** Descripción literal del estado de la operación.
    * **date (datetime):** Fecha y hora de la operación.
    * **order (string):** Ticket de la operación.
    * **masked_card (string):** Número de la tarjeta enmascarado.
    * **operation_name (string):** Nombre literal del tipo de operación.
    * **operation (string):** Identificador del tipo de operación.
    * **transaction_id (string):** Identificador de la transacción.
    * **status (string):** Identificador del estado de la operación.
    * **amount (Amount):** Importe de la operación.
    * **authorization_id (string):** Identificador de la entidad autorizadora.
    * **channel_name (string):** Nombre literal del canal de pago.
    * **channel (string):** Identificador del canal de pago.
    * **method (string):** Identificador del método de pago.
    * **method_name (string):** Identificador literal del método de pago.


* **Refund:**

  Este objeto añade lo atributos:
  * **amount (Amount):** Importe de la operación.
  * **order (string):** Ticket de la operación.
  * **card_trade (string):** Emisor de la tarjeta. Solicite más información.
  * **card_type (string):** Tipo de la tarjeta. Solicite más información.
  * **masked_card (string):** Número de la tarjeta enmascarado.
  * **reconciliation (string):** Identificador para la conciliación bancaria (p37).
  * **transaction_id (string):** Identificador de la transacción.
  * **aproval (string):** Código de aprobación de la entidad.
  * **authorizator (string):** Entidad autorizadora de la operación.


* **Register:**


* **card_mask (string):** Número de la tarjeta enmascarado
* **expired_at (date):** Fecha de la expiración
* **token (string):** Identificador de la tarjeta
* **card(StoredCard):** Objeto tarjeta asociado a la tarjeta devuelta.

* **Unregister:**

  Este objeto no añade nada a los atributos anteriores.

## **Ecommerce**

Para utilizar la SDK del middleware, hay que importar el paquete y crear el objeto con la ruta del archivo de configuración.

```python
  from sipay import Ecommerce
  ecommerce = Ecommerce('etc/config.ini')
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

Tras iniciar el objeto `ecommerce` se puede realizar las siguientes llamadas:
 * **Authorization**

  * **pay_method(PayMethod, required):** metodo de pago [Card, StoredCard, FastPay]
  * **amount(Amount, required):** importe de la operación
  * **order (string):** Ticket de la operación.
  * **reconciliation (string):** Identificador para la conciliación bancaria.
  * **custom_01 (string):** Campo personalizable.
  * **custom_02 (string):** Campo personalizable.
  * **token(string):** Si el método de pago no es una StoredCard, y el valor de token es un str no vacío almacena la tarjeta asociada el token pasado en este campo.

 Ejemplo:

 Autorización con tarjeta.

 ```python
   from sipay.paymethod.card import Card
   from sipay.amount import Amount

   amount = Amount(100, 'EUR') # 1€
   card = Card('0000000000000000', 2018, 2)

   auth = ecommerce.authorization(card, amount)
 ```

 Autorización con Fast Pay.

 ```python
   from sipay.paymethod.fastpay import FastPay
   from sipay.amount import Amount

   amount = Amount(100, 'EUR') # 1€
   fp = FastPay('830dc0b45f8945fab229000347646ca5')

   auth = ecommerce.authorization(fp, amount)
 ```

 El método authorization devuelve un objeto Authorization.

* **Refund**

  * **identificator(PayMethod or string):** Método de pago [Card, StoredCard, FastPay] o la id de transacción.
  * **amount (Amount, required):** Importe de la operación
  * **order (string):** Ticket de la operación.
  * **reconciliation (string):** Identificador para la conciliación bancaria.
  * **custom_01 (string):** Campo personalizable.
  * **custom_02 (string):** Campo personalizable.
  * **token(string):** Si el método de pago no es una StoredCard, y el valor de token es un str no vacío almacena la tarjeta asociada el token pasado en este campo.

  Ejemplo:

  Devolución con tarjeta.

  ```python
    from sipay.paymethod.storedcard import StoredCard
    from sipay.amount import Amount

    amount = Amount(100, 'EUR') # 1€
    card = StoredCard('bd6613acc6bd4ac7b6aa96fb92b2572a')

    refund = ecommerce.refund(card, amount)
  ```

  Devolución con transaction_id.

  ```python
    from sipay.amount import Amount

    amount = Amount(100, 'EUR') # 1€

    refund = ecommerce.refund('transaction_id', amount)
  ```

  El método refund devuelve un objeto Refund.

* **Register**

  * **card(Card, required):** Tarjeta a registrar.
  * **token(string, required):** Token con el que se le asocia a la tarjeta.

  Ejemplo:

  Registro de tarjeta.

  ```python
    from sipay.paymethod.card import Card

    card = Card('0000000000000000', 2018, 2)

    masked_card = ecommerce.register(card, 'newtoken')
  ```

  El método register devuelve un objeto Register.

* **Card**

  * **token(string, required):** Token asociado a la tarjeta.

  Ejemplo:

  Búsqueda de tarjeta.

  ```python
    masked_card = ecommerce.card('newtoken')
  ```

  El método card devuelve un objeto Card del apartado Responses.

* **Unregister**

  * **token(string, required):** Token asociado a la tarjeta.

  Ejemplo:

  Borrar una tarjeta del registro.

  ```python
    unregister = ecommerce.unregister('newtoken')
  ```

  El método unregister devuelve un objeto Unregister.

* **Cancellation**

  * **transaction_id(string, required):** identificador de la transacción.

  Ejemplo:

  Cancelación de operación.

  ```python
    cancel = ecommerce.cancellation('transaction_id')
  ```

  El método cancellation devuelve un objeto Cancellation.

* **Query**
  * **order(string):** Ticket de la operación.
  * **transaction_id(string):** identificador de la transacción.

  Ejemplo:

  Búsqueda de transacciones.

  ```python
    query = ecommerce.query(transaction_id='transaction_id')
  ```

  El método query devuelve un objeto Query.
