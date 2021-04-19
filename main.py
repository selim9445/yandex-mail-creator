from yandex import Yandex
from account import Account

account = Account()
account.generate_account()

yandex = Yandex(account, open("2captcha.apikey").read())
yandex.create_account()
