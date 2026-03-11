from rapidfuzz import fuzz
from rapidfuzz.process import extractOne

ALL_COMMANDS = [
    "hello",
    "help",
    "close",
    "exit",
    "add-contact",
    "edit-contact",
    "show-phone",
    "all-contacts",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "edit-email",
    "add-address",
    "edit-address",
    "find-contact",
    "delete-contact",
    "add-note",
    "all-notes",
    "find-note",
    "edit-note",
    "delete-note",
    "add-tag",
    "all-tags",
]

INTENT_KEYWORDS = {
    "hello": ["hello", "hi", "hey", "greet", "greeting"],
    "help": ["help", "commands", "what can you do", "how to use", "list commands", "menu"],
    "close": ["close", "exit", "quit", "bye", "goodbye"],
    "exit": ["close", "exit", "quit", "bye", "goodbye"],
    "add-contact": [
        "add contact", "new contact", "create contact", "save contact",
        "add person", "add number",
    ],
    "edit-contact": [
        "edit contact", "change phone", "change number", "update contact",
        "replace phone", "modify contact",
    ],
    "show-phone": [
        "show phone", "phone number", "get phone", "find number",
        "what is the number", "call", "dial",
    ],
    "all-contacts": [
        "all contacts", "show contacts", "list contacts", "display contacts",
        "show all contacts", "list all", "contacts list",
    ],
    "add-birthday": [
        "add birthday", "birthday", "date of birth", "set birthday",
        "when is birthday",
    ],
    "show-birthday": ["show birthday", "when is birthday", "birthday date", "get birthday"],
    "birthdays": [
        "upcoming birthdays", "birthdays", "who has birthday", "next birthdays",
    ],
    "add-email": ["add email", "add email address", "email", "contact email"],
    "edit-email": ["edit email", "change email", "update email", "new email"],
    "add-address": ["add address", "address", "contact address", "where does live"],
    "edit-address": ["edit address", "change address", "update address"],
    "find-contact": [
        "find contact", "search contact", "lookup contact", "find by name",
        "find by number", "search",
    ],
    "delete-contact": [
        "delete contact", "remove contact", "erase contact", "drop contact",
    ],
    "add-note": [
        "add note", "new note", "create note", "write note", "save note",
    ],
    "all-notes": [
        "all notes", "show notes", "list notes", "display notes", "notes list",
    ],
    "find-note": ["find note", "search note", "find notes", "search in notes"],
    "edit-note": ["edit note", "change note", "update note", "modify note"],
    "delete-note": ["delete note", "remove note", "erase note"],
    "add-tag": ["add tag", "tag note", "add tag to note", "label note"],
    "all-tags": ["all tags", "show tags", "list tags", "tags list"],
}

COMMAND_DESCRIPTIONS = {
    "hello": "Greet the assistant",
    "help": "Show list of commands",
    "close": "Exit the program",
    "exit": "Exit the program",
    "add-contact": "Add a new contact",
    "edit-contact": "Change contact phone",
    "show-phone": "Show phone by name",
    "all-contacts": "Show all contacts",
    "add-birthday": "Add birthday",
    "show-birthday": "Show birthday",
    "birthdays": "Upcoming birthdays",
    "add-email": "Add email to contact",
    "edit-email": "Change contact email",
    "add-address": "Add address",
    "edit-address": "Change address",
    "find-contact": "Find contact",
    "delete-contact": "Delete contact",
    "add-note": "Add a note",
    "all-notes": "Show all notes",
    "find-note": "Find notes",
    "edit-note": "Edit a note",
    "delete-note": "Delete a note",
    "add-tag": "Add tag to note",
    "all-tags": "Show all tags",
}

_INTENT_CHOICES = []
_COMMAND_FOR_CHOICE = []
for _cmd, _phrases in INTENT_KEYWORDS.items():
    for _phrase in _phrases:
        _INTENT_CHOICES.append(_phrase)
        _COMMAND_FOR_CHOICE.append(_cmd)

COMMAND_NAME_CUTOFF = 50
INTENT_PHRASE_CUTOFF = 45


def _make_suggestion(command):
    description = COMMAND_DESCRIPTIONS.get(command, command)
    return command, f"Maybe you meant: {command} — {description}"


def suggest_command(user_input):
    if not user_input or not user_input.strip():
        return None, None

    text = user_input.strip().lower()
    first_token = text.split()[0] if text else ""
    is_single_token = " " not in text

    if text and not is_single_token:
        result = extractOne(text, _INTENT_CHOICES, scorer=fuzz.token_set_ratio, score_cutoff=INTENT_PHRASE_CUTOFF)
        if result:
            _, _, idx = result
            return _make_suggestion(_COMMAND_FOR_CHOICE[idx])

    if first_token and is_single_token:
        result = extractOne(first_token, ALL_COMMANDS, scorer=fuzz.ratio, score_cutoff=COMMAND_NAME_CUTOFF)
        if result:
            best_cmd, _, _ = result
            return _make_suggestion(best_cmd)

    if text:
        result = extractOne(text, _INTENT_CHOICES, scorer=fuzz.token_set_ratio, score_cutoff=INTENT_PHRASE_CUTOFF)
        if result:
            _, _, idx = result
            return _make_suggestion(_COMMAND_FOR_CHOICE[idx])

    return None, None
