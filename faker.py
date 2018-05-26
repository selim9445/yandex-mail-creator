import random
import string
import os
import inspect


class Faker:

    @staticmethod
    def get_male_first_name():
        f = open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/FIRSTNAMES_m.txt', 'r')
        name = random.choice(f.readlines())
        name = name.lower()
        name = name[0].upper() + name[1:]
        return name.rstrip('\n')

    @staticmethod
    def get_female_first_name():
        f = open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/FIRSTNAMES_f.txt', 'r')
        name = random.choice(f.readlines())
        name = name.lower()
        name = name[0].upper() + name[1:]
        return name.rstrip('\n')

    @staticmethod
    def get_last_name():
        f = open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/LASTNAMES.txt', 'r')
        last_name = random.choice(f.readlines())
        last_name = last_name.lower()
        last_name = last_name[0].upper() + last_name[1:]
        return last_name.rstrip('\n')

    @staticmethod
    def generate_password(length):
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        random.seed = (os.urandom(1024))
        return ''.join(random.choice(chars) for i in range(length))

    @staticmethod
    def generate_gender():
        return random.choice(['female', 'male'])

    @staticmethod
    def generate_birth_day():
        return str(random.randint(1, 28))

    @staticmethod
    def generate_birth_month():
        return str(random.randint(1, 12))

    @staticmethod
    def generate_birth_year():
        return str(random.randint(1970, 1995))
