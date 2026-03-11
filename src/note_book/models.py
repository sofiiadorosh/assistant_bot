from collections import UserDict


class NoteBookError(Exception):
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
        tag = (tag or "").strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def edit_content(self, content):
        self.content = Content(content)

    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}, Tags: {', '.join(self.tags)}"


class NoteBook(UserDict):
    def add_note(self, note):
        self.data[note.title.value] = note

    def find_note_by_title(self, title):
        for stored, note in self.data.items():
            if stored.lower() == title.lower():
                return note
        return None

    def delete_note(self, title):
        del self.data[title]

    def find_note_by_keyword(self, keyword):
        return [
            note
            for note in self.data.values()
            if keyword in note.title.value.lower()
            or keyword in note.content.value.lower()
        ]

    def find_note_by_tag(self, tag):
        return [
            note
            for note in self.data.values()
            if any(tag == note_tag.lower() for note_tag in note.tags)
        ]

    def find_note(self, field, value):
        field = (field or "keyword").lower()
        if field == "tag":
            return self.find_note_by_tag(value)
        return self.find_note_by_keyword(value)

    def all_tags(self):
        return list(set(tag for note in self.data.values() for tag in note.tags))

    def sort_notes(self):
        return sorted(self.data.values(), key=lambda x: x.title.value)
