import re
from datetime import datetime

from colorama import init, Fore
init(autoreset=True)

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError(
                Fore.RED + 'Incorrect number format. Please enter a 10-digit number.')
        self.__value = value


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, value):
            raise ValueError(
                Fore.RED + 'Incorrect email format. Please enter email like user@example.com.')
        self.__value = value


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not datetime.strptime(value, "%d/%m/%Y"):
            raise ValueError(
                Fore.RED + 'Waiting format of date - DD/MM/YYYY. Reinput, please')
        else:
            self.__value = datetime.strptime(value, "%d/%m/%Y")

    def __str__(self):
        return self.value.strftime('%d/%m/%Y')


if __name__ == "__main__":
    pass
