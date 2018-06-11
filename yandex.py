import inspect
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import base64
import requests
from webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


class Yandex(WebDriver):

    def __init__(self, account=None, api_key=None):
        opts = Options()
        opts.add_experimental_option('prefs', {'intl.accept_languages': 'tr-TR,tr;q=0.8,en-US;q=0.6,en;q=0.4'})
        opts.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        WebDriver.__init__(self, opts)
        self.registerPage = 'https://mail.yandex.com/'
        self.apiKey = api_key
        self.account = account
        self.id = None

    def create_account(self):
        self.driver.get(self.registerPage)
        try:
            self.wait_until_page_loaded()
            if self.get_element(By.CLASS_NAME, 'lg-cc__button_type_action') is not None:
                self.get_element(By.CSS_SELECTOR, '.lg-cc__button_type_action').click()
                self.wait_element(By.CSS_SELECTOR, 'a[href^="https://passport.yandex.com/registration"]')
            self.get_element(By.CSS_SELECTOR, 'a[href^="https://passport.yandex.com/registration"]').click()
            self.wait_until_page_loaded()

            self.get_element(By.CSS_SELECTOR, '.link_has-no-phone').click()
            time.sleep(2)

            first_name_element = self.get_element(By.ID, 'firstname')
            last_name_element = self.get_element(By.ID, 'lastname')
            login_element = self.get_element(By.ID, 'login')

            self.send_slow_key(first_name_element, self.account.firstName)

            self.send_slow_key(last_name_element, self.account.lastName)

            self.send_slow_key(login_element, self.account.mail)

            self.wait_until_ajax_response()
            time.sleep(1)

            mail_retry_count = 0
            parent = self.get_parent_node(By.ID, 'login', 2)

            while 'field__error' in parent.get_attribute('class') and mail_retry_count < 3:
                login_element.clear()
                self.account.mail = self.account.mail + str(int(round(time.time() * 1000)))
                self.send_slow_key(login_element, self.account.mail)
                self.wait_until_ajax_response()
                time.sleep(1)
                mail_retry_count += 1
                if mail_retry_count == 3:
                    self.driver.quit()

            password_element = self.get_element(By.ID, 'password')
            self.send_slow_key(password_element, self.account.password)

            password_confirm_element = self.get_element(By.ID, 'password_confirm')
            self.send_slow_key(password_confirm_element, self.account.password)

            print('Email adresi {}@yandex.com ve sifre {} olarak belirlendi'.format(
                self.driver.find_element_by_id('login').get_attribute('value'), self.account.password))

            hint_answer = self.get_element(By.ID, 'hint_answer')
            if hint_answer.get_attribute('value').strip() == '':
                self.send_slow_key(hint_answer, self.account.firstName + ' ' + self.account.lastName)

            self.fill_other_fields()

        finally:
            self.driver.quit()

    def decode_capthca(self):
        captcha_element = self.get_element(By.CSS_SELECTOR, '.captcha__image')
        captcha_url = captcha_element.get_attribute('src')
        print('Capthca cozuluyor')
        b64_captcha = base64.b64encode(requests.get(captcha_url).content)
        id_result = requests.post("http://2captcha.com/in.php",
                                  data={'method': "base64", 'key': self.apiKey, 'body': b64_captcha, 'json': 0}).text

        id_result = id_result.split('|')
        self.id = id_result[1]

        print('Captcha id: ' + self.id)

        text_result = requests.get("http://2captcha.com/res.php?key=" + self.apiKey + "&action=get&id=" + self.id).text

        captcha_retry_count = 0

        while text_result == 'CAPCHA_NOT_READY' and captcha_retry_count < 5:
            print('Captcha is not ready, waiting')
            time.sleep(60)
            text_result = requests.get(
                "http://2captcha.com/res.php?key=" + self.apiKey + "&action=get&id=" + self.id).text
            captcha_retry_count += 1
            if captcha_retry_count == 5:
                self.driver.quit()
        print(text_result)
        text = text_result.split('|')
        text = text[1]

        print('Captcha cozuldu {}'.format(text))

        captcha_element = self.get_element(By.ID, 'captcha')
        captcha_element.clear()
        self.send_slow_key(captcha_element, text)

    def fill_other_fields(self):
        self.decode_capthca()
        self.wait_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
        confirm_registration_element.click()
        self.wait_until_ajax_response()
        time.sleep(1)

        for i in range(5):
            try:
                if self.get_element(By.CSS_SELECTOR, '.form__popup-error') is not None:
                    print('Hatali captcha.')
                    text_result = requests.get(
                        "http://2captcha.com/res.php?key=" + self.apiKey + "&action=reportbad&id=" + self.id).text
                    if text_result == 'OK_REPORT_RECORDED':
                        print('Hatali captcha rapor edildi')
                    time.sleep(0.5)
                    self.fill_other_fields()
                    return
            except NoSuchElementException:
                break
        if self.get_element(By.CLASS_NAME, 'eula-popup__show') is None:
            pass
        else:
            self.get_element(By.CSS_SELECTOR,
                             '#root > div > div.grid > div > main > div > div > div > form > div.form__submit > div > div.eula-popup > button').click()

        self.wait_until_page_loaded()
        time.sleep(2)

        try:
            form_button_enter = self.get_element(By.CSS_SELECTOR, '.new-hr-auth-Form_Button-enter')
            if form_button_enter is not None:
                form_button_enter.click()
                self.wait_until_page_loaded()

                new_login_element = self.get_element(By.CSS_SELECTOR, 'input[name="login"]')
                self.send_slow_key(new_login_element, self.account.mail)

                new_password_element = self.get_element(By.CSS_SELECTOR, 'input[name="passwd"]')
                self.send_slow_key(new_password_element, self.account.password)

                password_button_element = self.get_element(By.CSS_SELECTOR, '.passport-Button')
                password_button_element.click()
        except NoSuchElementException:
            pass

        self.wait_until_page_url('https://mail.yandex.com/?uid=')

        try:
            self.wait_element(By.CSS_SELECTOR, '.js-get-mobile-app-link-skip')
            self.get_element(By.CSS_SELECTOR, '.js-get-mobile-app-link-skip').click()
            time.sleep(1)
            self.get_element(By.CSS_SELECTOR, '.mail-WelcomeWizard-ThemeStep-Buttons-Link').click()
            time.sleep(1)
            self.get_element(By.CSS_SELECTOR, '.js-go-to-next-step').click()
            time.sleep(2)
            print('Yandex hesabi basariyla olusturuldu')
            file_path = os.path.dirname(
                os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/yandexaccounts.txt'
            with open(file_path, 'a') as file:
                file.write(self.account.mail + '@yandex.com:' + self.account.password + '\n')

        except NoSuchElementException:
            pass
