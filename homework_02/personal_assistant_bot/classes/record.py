from datetime import date

try:
   from classes.record_fields import Address, Birthday, Email, Name, Phone
except ModuleNotFoundError:
   from personal_assistant_bot.classes.record_fields import Address, Birthday, Email, Name, Phone

from colorama import init, Fore
init(autoreset=True)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = ""
        self.email = ""
        self.address = ""

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d/%m/%Y')}" if self.birthday else ""
        email_str = f", email: {self.email}" if self.email else ""       
        address_str = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}{email_str}{address_str}"

    def edit_name(self, edited_name):
        self.name = Name(edited_name)
        print(Fore.GREEN + f"Editing NAME to '{edited_name}' is successful!")

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        print(Fore.GREEN + f"Adding PHONE '{phone}' is successful!")

    def remove_phone(self, phone):
        for i in self.phones:
            if phone == i.value:
                self.phones.remove(i)
                print(Fore.GREEN + f"Removing PHONE '{phone}' is successful!")
                return True
        raise ValueError(Fore.RED + 'Incorrect number. Reinput, please')

    def edit_phone(self, old_phone, edited_phone):
        cash_phones = []
        for i in self.phones:
            cash_phones.append(i.value)
        if old_phone in cash_phones:
            new_phones = []
            for i in self.phones:
                if i.value == old_phone:
                    new_phones.append(Phone(edited_phone))
                else:
                    new_phones.append(Phone(i.value))
            self.phones = new_phones
            print(Fore.GREEN + f"Editing PHONE to '{edited_phone}' is successful!")
            return True
        else: 
            raise ValueError(Fore.RED + 'Incorrect number. Reinput, please')

    def find_phone(self, phone):
        cash_phones = []
        for i in self.phones:
            cash_phones.append(i.value)
        if phone in cash_phones:
            for i in self.phones:
                if phone == i.value:
                    return i
        else:
            print(Fore.RED + f"Phone number '{phone}' didn't find!")
            return None

    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
            print(Fore.GREEN + f"Adding BIRTHDAY '{birthday}' is successful!")
        else:
            print(Fore.RED + f"Record '{self.name}' yet have field birthday - '{self.birthday.value.strftime('%d/%m/%Y')}'")

    def edit_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)
        print(Fore.GREEN + f"Editing BIRTHDAY to '{new_birthday}' is successful!")

    def delete_birthday(self): #в завданні відсутній, але потрібний для консистентності
        pass 

    def days_to_birthday(self):
        if not self.birthday:
            return Fore.RED + f"Record '{self.name}' saved without birthday"
        today_date = date.today()
        birthday_date = date(today_date.year, self.birthday.value.month, self.birthday.value.day)
        if birthday_date < today_date:
            birthday_date = birthday_date.replace(year=today_date.year + 1)
        delta = birthday_date - today_date
        return delta.days

    def add_email(self, email):
        if not self.email:
            self.email = Email(email)
            print(Fore.GREEN + f"Adding EMAIL '{email}' is successful!")
        else:
            print(Fore.RED + f"Record '{self.name}' yet have field email - '{self.email.value}'")

    def edit_email(self, new_email):
        self.email = Email(new_email)
        print(Fore.GREEN + f"Editing EMAIL to '{new_email}' is successful!")

    def remove_email(self):
        if self.email:
            self.email = Email("")
            print(Fore.GREEN + f"Removing EMAIL '{self.email}' is successful!")
        else:
            print(Fore.RED + f"Record '{self.name}' don't have field email!")

    def add_address(self, address):
        if not self.address:
            self.address = Address(address)
            print(Fore.GREEN + f"Adding ADDRESS '{address}' is successful!")
        else:
            print(Fore.RED + f"Record '{self.name}' yet have field address - '{self.address.value}'")

    def edit_address(self, new_address):
        self.address = Address(new_address)
        print(Fore.GREEN + f"Editing ADDRESS to '{new_address}' is successful!")

    def remove_address(self):
        if self.address:
            del self.address
            print(Fore.GREEN + f"Removing ADDRESS '{self.address}' is successful!")
        else:
            print(Fore.RED + f"Record '{self.name}' don't have field address!")