from collections import UserDict


class NoteBookError(Exception):
    pass


class NoteNotFoundError(NoteBookError):
    pass


class InvalidTitleError(NoteBookError):
    pass


class InvalidContentError(NoteBookError):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value or not str(new_value).strip():
            raise InvalidTitleError("Title must not be empty.")
        self._value = str(new_value).strip()


class Content(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not new_value or not str(new_value).strip():
            raise InvalidContentError("Content must not be empty.")
        self._value = str(new_value).strip()


class Note:
    def __init__(self, title, content):
        self.title = Title(title)
        self.content = Content(content)
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}, Tags: {', '.join(self.tags)}"


class NoteBook(UserDict):
    def add_note(self, note):
        self.data[note.title.value] = note

    def find_note_by_title(self, title):
        if title not in self.data:
            return None
        return self.data[title]

    def delete_note(self, title):
        if title not in self.data:
            raise NoteNotFoundError(f"Note '{title}' not found.")
        del self.data[title]

    def find_note_by_keyword(self, keyword):
        return [
            note
            for note in self.data.values()
            if keyword in note.title.value or keyword in note.content.value
        ]

    def find_note_by_tag(self, tag):
        return [note for note in self.data.values() if tag in note.tags]

    def all_tags(self):
        return list(set(tag for note in self.data.values() for tag in note.tags))

    def sort_notes(self):
        return sorted(self.data.values(), key=lambda x: x.title.value)
