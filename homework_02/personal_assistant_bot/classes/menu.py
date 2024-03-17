try:
    from classes.note import Note
    from classes.notes import Notes
    from classes.record import Record
    from classes.addressbook import AddressBook
    from settings.settings import PAG, addressbook_filename, notes_filename
    from functions.functions import make_header, split_text, sort
except ModuleNotFoundError:
    from personal_assistant_bot.classes.note import Note
    from personal_assistant_bot.classes.notes import Notes
    from personal_assistant_bot.classes.record import Record
    from personal_assistant_bot.classes.addressbook import AddressBook
    from personal_assistant_bot.settings.settings import PAG, addressbook_filename, notes_filename
    from personal_assistant_bot.functions.functions import make_header, split_text, sort

from abc import ABC, abstractmethod
from colorama import Fore

class ShowObjMenu(ABC):

    @abstractmethod
    def show_menu(self):
        pass

class ObjMenuItemFunctionality(ABC):

    @abstractmethod
    def add_item(self):
        pass

    @abstractmethod
    def edit_item(self):
        pass

    @abstractmethod
    def find_items(self):
        pass

    @abstractmethod
    def remove_item(self):
        pass

    @abstractmethod
    def show_item(self):
        pass

    @abstractmethod
    def show_items(self):
        pass

    @abstractmethod
    def save_changes(self):
        pass

class NotesMenu(ShowObjMenu, ObjMenuItemFunctionality):

    def add_item(self, notesbook: Notes) -> None:

        make_header("ADD NOTE")

        note_text = input("\nInput note text: ")
        note_text = note_text.strip()

        print("\nInput note tags one per line (type 0 for finish):")
        note_tag = ""
        note_tags = []

        while True:
            note_tag = input("> ")
            if note_tag == "0":
                break
            note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
            if note_tag:
                note_tags.append(note_tag)

        if not note_text and not note_tags:
            print(Fore.GREEN + "\nNothing to add!")
            Fore.RESET
        else:
            notesbook.add_note(Note(note_text, tags=note_tags))

            print(Fore.GREEN + "\nSuccess!")
            Fore.RESET

            self.show_items(notesbook, uid=(notesbook.uid - 1))

            self.save_changes(notesbook)

        input("\nPress Enter to continue...")

    def edit_item(self, notesbook: Notes) -> None:

        make_header("EDIT NOTE")

        uid = input("\nInput note UID you want to edit: ")

        try:
            uid = int(uid)
            if not notesbook.is_note_exists(uid):
                raise ValueError
        except:
            print(Fore.RED + "\nA note with this UID does not exist!")
            Fore.RESET

            input("\nPress Enter to continue...")
            return

        self.show_items(notesbook, uid=uid)

        note_text = ""
        note_tags = []

        choice = input(
            "\nDo you want to edit the note text? (1 = yes / any key = no): ")

        if choice == "1":
            note_text = input("\nInput new note text: ")
            note_text = note_text.strip()

        choice = input(
            "\nDo you want to edit the note tags? (1 = yes / any key = no): ")

        if choice == "1":
            print("\nInput new note tags one per line (type 0 for finish):")
            note_tag = ""

            while True:
                note_tag = input("> ")
                if note_tag == "0":
                    break
                note_tag = note_tag.strip().replace(" ", "_").replace(",", "_")
                if note_tag:
                    note_tags.append(note_tag)

        if not note_text and not note_tags:
            print(Fore.GREEN + "\nNothing to change!")
            Fore.RESET

            input("\nPress Enter to continue...")
            return

        if note_text:
            notesbook.edit_note(uid, new_text=note_text)

        if note_tags:
            notesbook.edit_note(uid, new_tags=note_tags)

        print(Fore.GREEN + "\nSuccess!")
        Fore.RESET

        self.show_items(notesbook, uid=uid)

        self.save_changes(notesbook)

        input("\nPress Enter to continue...")

    def remove_item(self, notesbook: Notes) -> None:

        make_header("REMOVE NOTE")

        uid = input("\nInput note UID you want to remove: ")

        try:
            uid = int(uid)
            if not notesbook.is_note_exists(uid):
                raise ValueError
        except:
            print(Fore.RED + "\nA note with this UID does not exist!")
            Fore.RESET

            input("\nPress Enter to continue...")
            return

        self.show_items(notesbook, uid=uid)

        choice = input(
            "\nDo you want to remove this note? (1 = yes / any key = no): ")

        if choice == "1":
            notesbook.remove_note(uid)

            print(Fore.GREEN + "\nSuccess!")
            Fore.RESET

            self.save_changes(notesbook)

        input("\nPress Enter to continue...")

    def show_item(self, notesbook: Notes) -> None:

        make_header("SHOW NOTE")

        uid = input("\nInput note UID you want to show: ")

        try:
            uid = int(uid)
            if not notesbook.is_note_exists(uid):
                raise ValueError
        except:
            print(Fore.RED + "\nA note with this UID does not exist!")
            Fore.RESET

            input("\nPress Enter to continue...")
            return
        
        self.show_items(notesbook, uid=uid)

        input("\nPress Enter to continue...")

    def show_items(self, notesbook: Notes, uid=0, notes_list=[]) -> None:
        """
        Функція перегляду нотаток.
        Параметри відпрацьовують з наступним пріорітетом:
        1. Якщо заданий uid, то виводить нотатку з цим uid
        2. Якщо заданий notes_list, то виводить список нотаток
        3. Якщо не заданий жоден з цих параметрів - виводить всі нотатки
        """

        proc_list = []
        print_end = False

        if uid != 0:
            if notesbook.show_note(uid):
                proc_list.append(notesbook.show_note(uid))
            else:
                return
        elif notes_list:
            proc_list = notes_list
        else:

            make_header("SHOW ALL NOTES")

            proc_list = notesbook.show_all_notes()
            print_end = True

        print("-" * 141)
        print("|{:^5}|{:^40}|{:^40}|{:^25}|{:^25}|".format(
            'UID', 'Text', 'Tags', 'Created', 'Modified'))
        print("-" * 141)

        count = 0
        for item in proc_list:
            note_text = item[1].show_text()
            note_tags = item[1].show_tags()

            note_tags = ", ".join(note_tags)

            text_list = split_text(note_text)
            tags_list = split_text(note_tags)

            if len(split_text(note_text)) > 1:
                if len(split_text(note_tags)) > 1:
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        item[0], text_list[0], tags_list[0], item[2], item[3]))
                    for i in range(1, max(len(text_list), len(tags_list))):
                        text = text_list[i] if i < len(text_list) else ""
                        tag = tags_list[i] if i < len(tags_list) else ""
                        print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                            "", text, tag, "", ""))
                else:
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        item[0], text_list[0], note_tags, item[2], item[3]))
                    for i in range(1, len(text_list)):
                        print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                            "", text_list[i], "", "", ""))
            else:
                if len(split_text(note_tags)) > 1:
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        item[0], note_text, tags_list[0], item[2], item[3]))
                    for i in range(1, len(tags_list)):
                        print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                            "", "", tags_list[i], "", ""))
                else:
                    print("|{:^5}|{:<40}|{:<40}|{:^25}|{:^25}|".format(
                        item[0], note_text, note_tags, item[2], item[3]))
                    
            print("-" * 141)

            if count + 1 == PAG:
                count = 0
                choice = input("Press Enter to continue or 0 + Enter to break... ")            
                if choice == "0":
                    break
                else:
                    print("\n")
                    print("-" * 141)
                    continue
            else:
                count += 1

        if print_end:
            input("\nPress Enter to continue...")

    def save_changes(self, notesbook: Notes, p=False) -> None:

        if p:
            make_header("SAVE NOTES TO FILE")

        choice = input(
            "\nDo you want to save your changes? (1 = yes / any key = no): ")

        if choice == "1":
            try:
                notesbook.save_to_file(notes_filename)

                print(Fore.GREEN + "\nChanges saved successfully!")
                Fore.RESET

            except:
                print(Fore.RED + "\nError saving changes!")
                Fore.RESET

        if p:
            input("\nPress Enter to continue...")

    def find_items(self, notesbook: Notes) -> None:

        make_header("FIND NOTES")

        find_text = input("\nInput a search phrase: ")

        search_result = notesbook.find_notes(find_text)

        self.show_items(notesbook, notes_list=search_result)

        input("\nPress Enter to continue...")

    def sort_notes(self, notesbook: Notes) -> None:

        make_header("SORT NOTES")

        sort_by = ""
        sort_revers = False

        choice = input(
            "\nDo you want to sort by note text? (1 = yes / any key = no): ")

        if choice == "1":
            sort_by = "text"
        else:
            choice = input(
                "\nDo you want to sort by note tags? (1 = yes / any key = no): ")

            if choice == "1":
                sort_by = "tag"
            else:
                input("\nPress Enter to continue...")
                return

        choice = input("\nDo you want to sort by asc? (1 = yes / any key = no): ")

        if choice != "1":
            sort_revers = True

        sort_result = notesbook.sort_notes(sort_by=sort_by, revers=sort_revers)

        self.show_items(notesbook, notes_list=sort_result)

        input("\nPress Enter to continue...")

    def show_menu(self, notesbook: Notes) -> None:

        while True:

            make_header("NOTES MENU")

            print(
                """ 
1. Add note
2. Edit note (by UID)
3. Remove note (by UID)
4. Show note (by UID)
5. Show all notes
6. Find notes
7. Sort notes
8. Save notes to file

0. Exit to previous menu
"""
            )

            cmd = input("Choose an action: ")

            if cmd == "0":
                return
            elif cmd == "1":
                self.add_item(notesbook)
            elif cmd == "2":
                self.edit_item(notesbook)
            elif cmd == "3":
                self.remove_item(notesbook)
            elif cmd == "4":
                self.show_item(notesbook)
            elif cmd == "5":
                self.show_items(notesbook)
            elif cmd == "6":
                self.find_items(notesbook)
            elif cmd == "7":
                self.sort_notes(notesbook)
            elif cmd == "8":
                self.save_changes(notesbook, p=True)
            else:
                print("Wrong input!")

class RecordsMenu(ShowObjMenu, ObjMenuItemFunctionality):

    def add_item(self, addresssbook: AddressBook) -> None:

        make_header("ADD RECORD")

        name = input("\nPlease enter the name: ")
        new_record = Record(name)

        while True:
            phone = input("Please enter the phone: ")
            try:                                
                new_record.add_phone(phone)
            except ValueError:
                print(Fore.RED + 'Incorrect number format. Please enter a 10-digit number.')
            else:
                break

        while True:
            email = input("Please enter the email: ")
            try:                            
                new_record.add_email(email)
            except ValueError:
                print(Fore.RED + 'Incorrect email format. Please enter email like user@example.com.')
            else:
                break

        address = input("Please enter the address: ")
        new_record.add_address(address)

        while True:
            birthday = input("Please enter the date of birth in format DD/MM/YYYY: ")
            try:                                
                new_record.add_birthday(birthday)
            except ValueError:
                print(Fore.RED + 'Waiting format of date - DD/MM/YYYY. Reinput, please.')
            else:
                break

        addresssbook.add_record(new_record)
        print(Fore.GREEN + "\nRecord added successful!\n")

        addresssbook.appruve_record(new_record)

        input("\nPress Enter to continue...")

    def edit_item(self, addresssbook: AddressBook) -> None:

        make_header("EDIT RECORD")

        addresssbook.edit_record()

        input("\nPress Enter to continue...")

    def remove_item(self, addresssbook: AddressBook) -> None:

        make_header("DELETE RECORD")

        contact_name = input("\nPlease enter contact name you need to delete: ")
        print("")

        addresssbook.delete(contact_name)

        input("\nPress Enter to continue...")

    def show_item(self, addresssbook: AddressBook) -> None:
        pass

    def show_items(self, addresssbook: AddressBook) -> None:

        make_header("SHOW ALL RECORDS")

        addresssbook.iterator()

        input("\nPress Enter to continue...")

    def save_changes(self, addresssbook: AddressBook) -> None:

        make_header("SAVE ADDRESSBOOK")

        addresssbook.write_contacts_to_file(addressbook_filename)

        print(Fore.GREEN + "\nAddressBook saved successful!")

        input("\nPress Enter to continue...")

    def find_items(self, addresssbook: AddressBook) -> None:

        make_header("FIND RECORDS")

        find_string = input("\nPlease input Name of record, which you want find: ")

        #find_result = AddressBook()
        find_result = addresssbook.find_record(find_string)

        if find_result:
            print("")
            addresssbook.find_record(find_string).iterator_simple()
        else:
            print(
                Fore.RED + f"\nI can`t find any matches with '{find_string}'")

        input("\nPress Enter to continue...")

    def find_birthdays(self, addresssbook: AddressBook) -> None:

        make_header("N DAYS FROM BIRTHDAY")

        days_to_serch = input("\nPlease input number of days to search: ")
        print("")

        addresssbook.find_birthdays(days_to_serch).iterator()

        input("\nPress Enter to continue...")

    def show_menu(self, addresssbook: AddressBook) -> None:

        while True:

            make_header("ADDESSBOOK MENU")

            print(
                """ 
1. Add record
2. Edit record (by Name)
3. Remove record (by Name)
4. Show record (by Name)
5. Show all records
6. Find records
7. Show records with birthday in N days
8. Save records to file

0. Exit to previous menu
"""
            )

            cmd = input("Choose an action: ")

            if cmd == "0":
                return
            elif cmd == "1":
                self.add_item(addresssbook)
            elif cmd == "2":
                self.edit_item(addresssbook)
            elif cmd == "3":
                self.remove_item(addresssbook)
            elif cmd == "4":
                self.show_item(addresssbook)
            elif cmd == "5":
                self.show_items(addresssbook)
            elif cmd == "6":
                self.find_items(addresssbook)
            elif cmd == "7":
                self.find_birthdays(addresssbook)
            elif cmd == "8":
                self.save_changes(addresssbook)
            else:
                print("Wrong input!")

class MainMenu(ShowObjMenu):

    def show_menu(self):

        while True:

            make_header("MAIN MENU")

            print(
                """ 
1. About Bot Helper
2. Hello, User!
3. Use Records
4. Use Notes
5. Sort Files in Folder

0. Exit
"""
            )

            cmd = input("Choose an action: ")

            if cmd == "0":
                return
            
            elif cmd == "1":

                make_header("ABOUT BOT HELPER")

                print("\nI'm a great bot and I will facilitate your work, now I will describe what I can do\n"
                        "I can work with contact: add, edit, remove contact's phone, email, birthday, address.\nAlso "
                        "I can work with your notes: add, edit, remove, show note or all notes, find and sort notes.\n"
                        "And finally, I have very useful function - sort, it helps you to sort all your files in "
                        "some directory. \nWhere do you want to start?")
                
                input("\nPress Enter to continue...")

            elif cmd == "2":

                make_header("HELLO, USER!")

                print('\nHello! How are you today? Are you ready to work?')

                input("\nPress Enter to continue...")

            elif cmd == "3":
                addressbook = AddressBook()
                addressbook = AddressBook.read_contacts_from_file(addressbook_filename)
                RecordsMenu().show_menu(addressbook)

            elif cmd == "4":
                notes = Notes().load_from_file(notes_filename)
                NotesMenu().show_menu(notes)

            elif cmd == "5":

                make_header("SORT FILES IN FOLDER")

                print(Fore.RED + "\nCarefully! Files will be sorted! You won't be able to find them in your usual place!")

                folder = input("\nPlease input folder name or press Enter to exit: ")

                if not folder:
                    pass
                else:
                    sort(folder)

                    print(Fore.GREEN + f"\nFiles and folders in {folder} sorted successful!")

                    input("\nPress Enter to continue...")

            else:
                print("Wrong input!")
