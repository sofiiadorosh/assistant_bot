# Personal Assistant Bot

A command-line interface (CLI) personal assistant application for managing contacts and notes.

## Features

### Contact Management

- **Add contacts** with the following information:
  - Name
  - Address
  - Phone number(s)
  - Email address
  - Birthday
- **Find contacts** by query (default: search all fields) or by field: name, phone, email, address, or all
- **Edit and delete** contact records
- **Birthday reminders** - display contacts with upcoming birthdays within a specified number of days
- **Input validation** - automatic validation of phone numbers and email addresses during creation or editing, with user notifications for invalid input

### Notes Management

- **Add notes** with title and content
- **Search notes** by various criteria (e.g., by keyword or tag)
- **Edit and delete** notes
- **Add tags** to notes and list all tags

### Intelligent Analysis

- **Command suggestions** - the assistant guesses what the user wants based on input text and suggests the closest matching command

### Data Persistence

- All data (contacts, notes) is stored on the local disk in the user's home directory
- The assistant can be restarted without losing any data

## Installation

```bash
# Clone the repository
git clone https://github.com/sofiiadorosh/assistant_bot.git
cd assistant_bot

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the assistant
python main.py
```

### Available Commands

#### General Commands

| Command | Description |
|---------|-------------|
| `hello` | Greet the assistant and see available commands hint |
| `help` | Display all available commands |
| `close` / `exit` | Exit the assistant |

#### Contacts

| Command | Description                                                                  |
|---------|------------------------------------------------------------------------------|
| `add-contact <name> <phone>` | Add a new contact with name and phone number                                 |
| `all-contacts` | Display all contacts                                                         |
| `find-contact <query>` or `find-contact <field> <query>` | Find contacts by all (default) or by field. Omit field to search all; use `name`, `phone`, `email`, `address`, or `all` to choose. |
| `delete-contact <name>` | Delete a contact                                                             |

#### Phone

| Command | Description |
|---------|-------------|
| `edit-contact <name> <old_phone> <new_phone>` | Change a contact's phone number |
| `show-phone <name>` | Show phone number(s) for a contact |

#### Birthday

| Command | Description |
|---------|-------------|
| `add-birthday <name> <date>` | Add a birthday to a contact (DD.MM.YYYY) |
| `show-birthday <name>` | Show birthday for a contact |
| `birthdays <days>` | Show contacts with birthdays in the next N days |

#### Email

| Command | Description |
|---------|-------------|
| `add-email <name> <email>` | Add an email address to a contact |
| `edit-email <name> <new_email>` | Update an existing email address |

#### Address

| Command | Description |
|---------|-------------|
| `add-address <name> <address>` | Add a physical address to a contact |
| `edit-address <name> <new_address>` | Update an existing physical address |

#### Notes

| Command | Description |
|---------|-------------|
| `add-note <title> <content>` | Add a new note |
| `all-notes` | Display all notes |
| `find-note <value>` or `find-note <field> <value>` | Find notes by keyword (default) or tag. Omit field to search by keyword; use `keyword` or `tag` to choose. |
| `edit-note <title> <content>` | Edit an existing note |
| `delete-note <title>` | Delete a note |
| `add-tag <title> <tag>` | Add a tag to a note |
| `all-tags` | Show all tags |

### Short commands

You can run commands using short form: **first word = action**, **second word = entity**, then the rest of the arguments. Same as the full commands above.

There are single-letter commands to get a list of all items: `c` = all contacts, `n` = all notes, `t` = all tags. For upcoming birthdays, `b` = birthdays: if you pass `b` with no argument it defaults to **7** days; otherwise it uses the number of days you entered (e.g. `b 14`).

| Action (1st word) | Entity (2nd word) |
|-------------------|-------------------|
| `a` add | `c` contact       |
| `e` edit | `n` note          |
| `d` delete | `p` phone         |
| `s` show | `e` email         |
| `f` find | `a` address       |
| | `b` birthday      |
| | `t` tag           |

**Examples:**
- `a c John 1234567890` → add contact John with phone 1234567890
- `f c name Henry` → find contacts by name
- `f c all John` → search all fields for "John"
- `a n Yupi Super dog` → add note
- `d n Yupi` → delete note
- `c` → all contacts (same as `all-contacts`)
- `n` → all notes (same as `all-notes`)
- `t` → all tags (same as `all-tags`)
- `b` → upcoming birthdays in the next 7 days (default); `b 14` → next 14 days

## Data Storage

All data (contacts, notes) is stored on the hard drive in the user's folder:
- The assistant can be restarted without losing any data
- Data is saved automatically after each operation

## Validation Rules

### Contacts

#### Name
- Must be at least 2 characters long (after trimming whitespace)
- Cannot be empty

#### Phone
- Must contain only digits
- At least 10 digits (e.g., `12025551234`)

#### Email
- Must follow standard email format (e.g., `user@example.com`)

#### Birthday
- Must be in date format **DD.MM.YYYY** (e.g., `25.12.1990`)

#### Address
- Must be at least 3 characters long (after trimming whitespace)

### Notes

#### Title
- Cannot be empty or only whitespace

#### Content
- Cannot be empty or only whitespace

## Project Structure

```
assistant_bot/
├── main.py                 # Application entry point
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
├── .gitignore
├── samples/                # Sample data (JSON)
│   ├── contacts.json       # Sample contacts
│   └── notes.json          # Sample notes
└── src/
    ├── __init__.py         # Package initialization
    ├── cli.py              # Command-line interface and input parsing
    ├── commands.py         # General commands (hello, help, exit)
    ├── decorators.py       # Input error handling, persist_data
    ├── exceptions.py       # Custom exception classes
    ├── address_book/       # Contact management
    │   ├── commands.py     # Contact command handlers
    │   ├── models.py       # AddressBook, Record, field models
    │   └── store.py        # Load/save contacts (JSON)
    └── note_book/          # Notes management
        ├── commands.py     # Note command handlers
        ├── models.py       # NoteBook, Note, Title, Content, tags
        └── store.py        # Load/save notes (JSON)
```

## Technologies

- Python 3.8+

## Contributing

1. Clone the repository (`git clone https://github.com/sofiiadorosh/assistant_bot.git`)
2. Create a feature branch (`git checkout -b feature/tags`)
3. Commit your changes (`git commit -m 'feat: add tags logic'`)
4. Push to the branch (`git push origin feature/tags`)
5. Open a Pull Request

## Commit Convention

Commit messages must follow these rules:
- Type must be lowercase (`feat`, `fix`, `refactor`, `docs`, `style`, `chore`, etc.)
- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")

### Commit Types

| Type | Description |
|------|-------------|
| `init` | Start of project/task (`init: start project`) |
| `feat` | New feature (`feat: add search box`) |
| `fix` | Bug fix (`fix: correct data loading`) |
| `refactor` | Code restructuring without behavior change (`refactor: rename vars`) |
| `docs` | Documentation changes (`docs: update readme`) |
| `style` | Code formatting (`style: format with prettier`) |
| `chore` | Maintenance tasks (`chore: add .editorconfig`) |
