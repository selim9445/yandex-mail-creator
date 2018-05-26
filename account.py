from faker import Faker


class Account:

    def __init__(self):
        self.firstName = None
        self.lastName = None
        self.mail = None
        self.password = None
        self.birthDay = None
        self.birthMonth = None
        self.birthYear = None
        self.gender = None
        self.cookie = None
        self.facebookID = None
        self.signedRequest = None
        self.accessToken = None
        self.refCode = None

    def generate_account(self):
        self.gender = Faker.generate_gender()
        if self.gender == 'male':
            self.firstName = Faker.get_male_first_name()
        else:
            self.firstName = Faker.get_female_first_name()
        self.lastName = Faker.get_last_name()
        self.mail = self.firstName.lower() + self.lastName.lower()
        self.password = Faker.generate_password(10)
        self.birthDay = Faker.generate_birth_day()
        self.birthMonth = Faker.generate_birth_month()
        self.birthYear = Faker.generate_birth_year()
