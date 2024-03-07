from collections import UserDict
from datetime import datetime
import pickle

try:
   from classes.note import Note
except ModuleNotFoundError:
   from personal_assistant_bot.classes.note import Note

class Notes(UserDict):

    uid = 1

    def __init__(self, *args):

        super().__init__()

        for item in args:
            if not isinstance(item, Note):
                raise TypeError
            else:
                self.data.setdefault(self.uid, []).append(item)
                self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
                self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
                self.uid += 1

    def add_note(self, note):

        if not isinstance(note, Note):
            raise TypeError

        self.data.setdefault(self.uid, []).append(note)
        self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        self.data[self.uid].append(datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        self.uid += 1

        return self

    def edit_note(self, uid, new_text="", new_tags=[]):

        if self.data.get(uid, None):

            if new_text:
                self.data[uid][0] = self.data[uid][0].edit_text(new_text)
                self.data[uid][2] = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

            if new_tags:
                old_tags = self.data[uid][0].show_tags()
                tags_to_remove = []

                for tag in old_tags:
                    if tag in new_tags:
                        continue
                    else:
                       tags_to_remove.append(tag)

                self.data[uid][0] = self.data[uid][0].remove_tags(tags_to_remove)
                self.data[uid][0] = self.data[uid][0].add_tags(new_tags)

                self.data[uid][2] = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")

        return self

    def remove_note(self, uid):

        if self.data.get(uid, None):
            self.data.pop(uid)

        return self

    def show_note(self, uid):
        
        if self.data.get(uid, None):
            return [uid, *self.data[uid]]
        else:
            return None

    def show_all_notes(self):

        result = []

        for key in self.data.keys():
            result.append(self.show_note(key))

        return result

    def find_notes(self, find_str):

        if type(find_str) != str:
            raise TypeError

        result = []
        find_tag = False

        for key, value in self.data.items():
            note_text = value[0].show_text()
            note_tags = value[0].show_tags()

            for tag in note_tags:
                if tag.lower().find(find_str.lower()) != -1:
                    result.append(self.show_note(key))
                    find_tag = True
                    break
            
            if find_tag:
                continue

            if note_text.lower().find(find_str.lower()) != -1:
                result.append(self.show_note(key))

        return result

    def sort_notes(self, sort_by="text", revers=False):

        is_sorted = False

        proc_list = self.show_all_notes()

        if sort_by == "text":

            while not is_sorted:
                is_sorted = True
                for i in range(0, len(proc_list) - 1):
                    for j in range(i + 1, len(proc_list)):
                        if proc_list[i][1].show_text() > proc_list[j][1].show_text():
                            proc_list[i], proc_list[j] = proc_list[j], proc_list[i]
                            is_sorted = False

        elif sort_by == "tag":

            while not is_sorted:
                is_sorted = True
                for i in range(0, len(proc_list) - 1):
                    for j in range(i + 1, len(proc_list)):
                        if proc_list[i][1].show_tags()[0] > proc_list[j][1].show_tags()[0]:
                            proc_list[i], proc_list[j] = proc_list[j], proc_list[i]
                            is_sorted = False

        if revers:
            proc_list = proc_list[::-1]

        return proc_list                

    def is_note_exists(self, uid):

        if self.data.get(uid, None):
            return True

        return False

    def save_to_file(self, notes_filename):
        with open(notes_filename, "wb") as file:
            pickle.dump(self, file)

    def load_from_file(self, notes_filename):

        try:
            with open(notes_filename, "rb") as file:
                self = pickle.load(file)
             
        except:
            
            self.add_note(Note("Не забути привітати товариша з днем народження",
                               tags=["ДР", "Поздоровити"]))

            self.add_note(Note("Купити навушники до вихідних",
                               tags=["Покупки"]))

            self.add_note(Note("Тестова нотатка",
                               tags=["AAA", "Test"]))

            self.add_note(Note("Відсортувати фотографії на своєму ПК за минулий рік",
                               tags=["2023", "Фото"]))

            self.add_note(Note("Забрати машину з ремонту",
                               tags=["Авто", "Забрати"]))

            self.add_note(Note("Тестова нотатка де багато тексту, щоб він був на декількох стрічках при виводі. Думаю, такого об'єму буде достатньо",
                               tags=["Багато", "В", "Для", "Нотаток", "Нотатці", "Тестування", "Цій"]))

            self.add_note(Note("Дати інформацію в відділ кадрів про відпустку",
                               tags=["Відпустка"]))

            self.add_note(Note("Ще одна нотатка для нагадування поздоровити з днем народження сестру",
                               tags=["Поздоровлення", "Сестра"]))

            self.add_note(Note("Купити коту корм після роботи",
                          tags=["Кіт", "Покупки"]))

        return self

    def __repr__(self):

        out = ""

        for key, value in self.data.items():
            out += f'id={key}, {value[0]}, created={value[1]}, last_modified={value[2]}\n'

        return out


if __name__ == "__main__":
    pass