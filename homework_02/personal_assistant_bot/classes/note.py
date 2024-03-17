class Note:

    def __init__(self, text="", tags=[]):

        if type(text) != str or type(tags) != list:
            raise TypeError

        self.text = text

        for item in tags:
            if type(item) != str:
                raise TypeError

        self.tags = list(set(tags))
        self.tags.sort()

    def edit_text(self, data):

        if type(data) != str:
            raise TypeError

        self.text = data

        return self

    def show_text(self):

        return self.text

    def add_tags(self, data):

        proc_tags = []

        if type(data) == str:
            if data not in self.tags:
                proc_tags.append(data)
        elif type(data) == list:
            for item in data:
                if type(item) == str:
                    if item not in self.tags:
                        proc_tags.append(item)
                else:
                    raise TypeError
        else:
            raise TypeError

        self.tags.extend(list(set(proc_tags)))
        self.tags.sort()

        return self

    def edit_tag(self, current_tag, new_tag):

        if type(new_tag) != str:
            raise TypeError

        if current_tag in self.tags:
            idx = self.tags.index(current_tag)

            self.tags[idx] = new_tag

        return self

    def remove_tags(self, data):

        if type(data) == str:
            if data in self.tags:
                self.tags.remove(data)
        elif type(data) == list:
            for item in data:
                if item in self.tags:
                    self.tags.remove(item)
        else:
            pass

        return self

    def show_tags(self):

        return self.tags

    def is_in_tags(self, data):

        return (data in self.tags)

    def __str__(self):

        return f'Note(text="{self.text}", tags={self.tags})'

    def __repr__(self):

        return f'Note(text="{self.text}", tags={self.tags})'


if __name__ == "__main__":
    pass