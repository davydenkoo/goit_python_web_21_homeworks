from collections import UserDict
from datetime import date, timedelta
import pickle

try:
   from classes.record import Record
   from settings.settings import addressbook_filename, PAG
except ModuleNotFoundError:
   from personal_assistant_bot.classes.record import Record
   from personal_assistant_bot.settings.settings import addressbook_filename, PAG

from colorama import init, Fore
init(autoreset=True)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self:
            for i in self:
                if i == name:
                    return self.data[i]
        else:
            return None

    def delete(self, name):
        if name in self:
            for i in self:
                if i == name:
                    self.data.pop(name)
                    self.write_contacts_to_file(addressbook_filename)
                    print(Fore.GREEN + f"Record '{name}' deleted successful!")
                    return True
        else:
            print(Fore.RED + f"Record '{name}' not found!")
            return None

    def iterator_simple(self):
        st_list, obj_len = [], len(self.data)

        for i, (name, record) in enumerate(self.data.items(), 1):
            st_list.append(str(record))
            if i % PAG == 0:
                print('\n'.join(st_list))
                st_list.clear()
                if i != obj_len and input(f"-->You can ^^see^^ {i} records from {obj_len}\n-->press any key to continue or 'q' to exit --> ").lower() == "q":
                    break
        if st_list:
            print('\n'.join(st_list))
        print(f"-->You can ^^see^^ {i} records from {obj_len}\n")

    def iterator(self):
        obj_len = len(self.data)
        i = 0

        def generate_records():
            for name, record in self.data.items():
                yield str(record)

        record_generator = generate_records()
        while True:
            portion = [next(record_generator, None) for _ in range(PAG)]
            portion = [item for item in portion if item is not None]  # Исключить None (когда записи закончились)
            i += len(portion)
            print('\n'.join(portion))
            if not portion or i == obj_len:
                print(f"-->You can ^^see^^ {i} records from {obj_len}\n")
                break
            if input(f"-->You can ^^see^^ {i} records from {obj_len}\n-->press any key to continue or 'q' to exit --> ").lower() == "q":
                break
        
    def find_record(self, find_string):
        find_string = find_string.lower()

        book = AddressBook()
        for i, (name, record) in enumerate(self.data.items(), 1):
            if find_string.isdigit():
                for phone in record.phones:
                    if str(phone).find(find_string) > -1:
                        book.add_record(record)
            else:
                if name.lower().find(find_string) > -1:
                    book.add_record(record)
        return book
    
    def find_birthdays(self, number):
        book = AddressBook()
        try:
            number_days = int(number)            
            today_date = date.today()
            chek_day  = today_date + timedelta(days=number_days)
            for i, (name, record) in enumerate(self.data.items()):
                if record.birthday:
                    cheked_day = record.birthday.value.date()
                    cheked_day = cheked_day.replace(year=today_date.year)
                    if cheked_day < today_date:
                        cheked_day = cheked_day.replace(year=today_date.year + 1)
                    if cheked_day < chek_day and cheked_day > today_date:
                        book.add_record(record)
        except ValueError:
            print(Fore.RED + "You must input number days")
        finally:
            return book

    @classmethod
    def fill_AdressBook(cls):

        book = cls()

        john_record1 = Record("John Black")
        john_record1.add_phone("1234567890")
        john_record1.add_email("johnblack@gmail.com")
        john_record1.add_address("00000, Kyiv, 125")
        book.add_record(john_record1)

        jane_record1 = Record("Jane Smile")
        jane_record1.add_phone("9876543210")
        jane_record1.add_birthday("01/01/2000")
        book.add_record(jane_record1)

        john_record2 = Record("Johnson")
        john_record2.add_phone("1234567890")
        john_record2.add_birthday("01/01/2002")
        john_record2.add_email("johnson@gmail.com")
        book.add_record(john_record2)

        jane_record2 = Record("Jane M")
        jane_record2.add_phone("9876543210")
        jane_record2.add_birthday("01/06/2024")
        book.add_record(jane_record2)

        john_record3 = Record("John3")
        john_record3.add_phone("1234567890")
        john_record3.add_address("00055, Kyiv, 1")
        book.add_record(john_record3)

        jane_record3 = Record("Janet")
        jane_record3.add_phone("9876543210")
        jane_record3.add_email("janet@gmail.com")
        jane_record3.add_address("00005, Kyiv, 100")
        book.add_record(jane_record3)

        book.write_contacts_to_file(addressbook_filename)

        return book
    

    def write_contacts_to_file(self, addressbook_filename):
        with open(addressbook_filename, "wb") as fh:
            pickle.dump(self, fh)
    
    @classmethod
    def read_contacts_from_file(cls, addressbook_filename):
        book = cls()
        try:
            with open(addressbook_filename, "rb") as fh:
                book = pickle.load(fh)
            return book
        except:
            print(Fore.RED + "File with recors was deleted or was never created!")
            print(Fore.GREEN + "I created a file with a records for example!")
            return book.fill_AdressBook()
    
    def appruve_record(self, new_record):
        print(new_record)
        print('''\nWhat You will do with this record?
1 - Save changes
2 - Discard changes''')
        choise = input()
        if choise == "1":
            self.write_contacts_to_file(addressbook_filename)
            print(Fore.GREEN + "Changes saved successful")
        elif choise == "2":
            self.delete(new_record)
            print(Fore.GREEN + "Changes discard successful")



    def edit_record(self):

        contact_name = input("\nPlease enter the name of the contact what you want to change: ")
        find_record = self.find(contact_name)
        if find_record is None:
            print(Fore.RED + "\nContact name not found!")
        else:
            edit_record_menu = '''\nEdit Record menu:
1. Edit Name
2. Edit Phone
3. Edit Birthday
4. Edit Email
5. Edit Address
6. Save and Exit
7. Exit'''
            edit_swither = True
            while  edit_swither:
                print("")
                print(find_record)
                print(edit_record_menu)
                choice = input("\nPlease input your choice: ")
                if choice == '7':
                    break
                elif choice == "1":
                    new_name = input("Please enter new Name: ")
                    print("")
                    find_record.edit_name(new_name)
                    if new_name != contact_name:
                        self.add_record(find_record)
                        self.delete(contact_name)
                elif choice == "2":
                    while True:
                        new_phone = input("Please enter new Phone: ")
                        print("")
                        try:
                            find_record.add_phone(new_phone)
                        except:
                            pass
                        else:
                            break
                elif choice == "3":
                    while True:
                        new_birthday = input("Please enter new Birthday in format DD/MM/YYYY: ")
                        print("")
                        try:
                            find_record.edit_birthday(new_birthday)
                        except:
                            pass
                        else:
                            break
                elif choice == "4":
                    while True:
                        new_email = input("Please enter new Email: ")
                        print("")
                        try:
                            find_record.edit_email(new_email)
                        except:
                            pass
                        else:
                            break
                elif choice == "5":
                    new_address = input("Please enter new Address: ")
                    print("")
                    find_record.edit_address(new_address) 
                elif choice == "6":
                    self.write_contacts_to_file(addressbook_filename)
                    print(Fore.GREEN + "\nChanges saved successful")
                    break
