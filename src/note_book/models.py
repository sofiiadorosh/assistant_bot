from collections import UserDict

class NoteNotFoundError(ValueError):
    pass


class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)

    def __str__(self):
        return f"Title: {self.title}, Content: {self.content}, Tags: {', '.join(self.tags)}"


class NoteBook(UserDict):
    def add_note(self, note):
        self.data[note.title] = note

    def find_note(self, title):
        if title not in self.data:
            return None
        return self.data[title]

    def delete_note(self, title):
        if title not in self.data:
            raise NoteNotFoundError(f"Note '{title}' not found.")
        del self.data[title]

    def search_notes(self, query):
        return [note for note in self.data.values() if query in note.title or query in note.content]

    def find_notes(self, tag):
        return [note for note in self.data.values() if tag in note.tags]

    def all_tags(self):
        return list(set(tag for note in self.data.values() for tag in note.tags))

    def sort_notes(self):
        return sorted(self.data.values(), key=lambda x: x.title)
