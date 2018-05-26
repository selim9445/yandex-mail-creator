from yandex import Yandex
from account import Account

account = Account()
account.generate_account()

yandex = Yandex(account, '2capthca-api-key')
yandex.create_account()
