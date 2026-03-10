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
- **Search contacts** by various criteria (e.g., by name)
- **Edit and delete** contact records
- **Birthday reminders** - display contacts with upcoming birthdays within a specified number of days
- **Input validation** - automatic validation of phone numbers and email addresses during creation or editing, with user notifications for invalid input

### Notes Management

- **Add text notes** with custom content
- **Search notes** by keywords
- **Edit and delete** notes

### Additional Features (Tags)

- **Add tags** to notes - keywords that describe the topic and subject of the note
- **Search and sort notes** by tags/keywords

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

#### Contact Commands

| Command | Description |
|---------|-------------|
| `add-contact <name> <phone>` | Add a new contact with name and phone number |
| `edit-contact <name> <old_phone> <new_phone>` | Change a contact's phone number |
| `show-phone <name>` | Show phone number(s) for a contact |
| `all-contacts` | Display all contacts |
| `add-birthday <name> <date>` | Add a birthday to a contact (DD.MM.YYYY) |
| `show-birthday <name>` | Show birthday for a contact |
| `birthdays <days>` | Show contacts with birthdays in the next N days |
| `add-email <name> <email>` | Add an email address to a contact |
| `edit-email <name> <new_email>` | Update an existing email address |
| `add-address <name> <address>` | Add a physical address to a contact |
| `edit-address <name> <new_address>` | Update an existing physical address |
| `search-contacts <field> <query>` | Search contacts by field: `name`, `phone`, `email`, `address`, or `all` |
| `delete-contact <name>` | Delete a contact |

#### Notes Commands

| Command | Description |
|---------|-------------|
| `add-note <title> <text>` | Add a new note |
| `all-notes` | Display all notes |
| `find-note <field> <value>` | Find notes by keyword or tag (field: `keyword` or `tag`) |
| `edit-note <title> <new_text>` | Edit an existing note |
| `delete-note <title>` | Delete a note |
| `add-tag <title> <tag>` | Add a tag to a note |
| `all-tags` | Show all tags |

## Data Storage

All data (contacts, notes) is stored on the hard drive in the user's folder:
- The assistant can be restarted without losing any data
- Data is saved automatically after each operation

## Validation Rules

### Phone Number
- Must contain only digits
- Should be a valid phone number format (e.g., 10+ digits)

### Email
- Must follow standard email format (e.g., `user@example.com`)
- Validated using regex pattern matching

### Birthday
- Must be in a valid date format (DD.MM.YYYY)
- Cannot be a future date

### Address
- Must be at least 3 characters long.

## Project Structure

```
assistant_bot/
├── main.py                 # Application entry point
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
└── src/
    ├── __init__.py         # Package initialization
    ├── cli.py              # Command-line interface and input parsing
    ├── commands.py         # General command handlers (hello, help, exit)
    ├── decorators.py       # Decorator functions (input error handling, persist_data)
    ├── exceptions.py       # Custom exception classes
    ├── address_book/       # Contact management
    │   ├── commands.py     # Contact command handlers
    │   ├── models.py       # AddressBook, Record, and contact-related models
    │   └── store.py        # Address book persistence (load/save)
    └── note_book/          # Notes management
        ├── commands.py     # Note command handlers
        ├── models.py       # NoteBook, Note, and tag models
        └── store.py        # Note book persistence (load/save)
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
