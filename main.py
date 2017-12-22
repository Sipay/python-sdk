"""Main."""
from mdwr import MDWR
from mdwr.paymethod.card import Card
from mdwr.paymethod.fastpay import FastPay
from mdwr.amount import Amount

mdwr = MDWR('etc/config.ini')

amount = Amount(100, 'EUR')

card_pan = Card(('6712009000000205', 2018, 2))
card_token = Card('bd6613acc6bd4ac7b60296fb92b2572a')
fp = FastPay('830dc0b45f8945fab229000347646ca5')

print('\nAuthorization:\n')

auth_pan = mdwr.authorization(card_pan, amount)
auth_token = mdwr.authorization(card_token, amount)
auth_fp = mdwr.authorization(fp, amount)

print(auth_token)
print(auth_pan)
print(auth_fp)

print('\nRefund:\n')

refund_pan = mdwr.refund(card_pan, amount)
refund_token = mdwr.refund(card_token, amount)
refund_fp = mdwr.refund(fp, amount)
refund_id = mdwr.refund(auth_pan.transaction_id, amount)

print(refund_token)
print(refund_pan)
print(refund_fp)
print(refund_id)

print('\nRegister:\n')

register = mdwr.register(card_pan, 'newtoken')

print(register)

print('\nCard:\n')

card_res = mdwr.card('newtoken')

print(card_res)

print('\nUnregister:\n')

unregister = mdwr.unregister('newtoken')

print(unregister)

print('\nCancel:\n')

cancel = mdwr.cancellation(auth_pan.transaction_id)

print(cancel)

print('\nQuery:\n')

query = mdwr.query(auth_pan.transaction_id)

print(query)
