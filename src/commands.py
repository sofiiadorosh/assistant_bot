from src.decorators import persist_data


def hello(args, contacts, notes):
    return "Welcome! Type 'help' to see available commands. How can I help you?"


@persist_data
def exit_program(args, contacts, notes):
    return "exit"


def show_help(args, contacts, notes):
    return """
+-----------------------------------------------+------------------------------------------------+
| Command                                       | Description                                    |
+-----------------------------------------------+------------------------------------------------+
| GENERAL                                                                                        |
+-----------------------------------------------+------------------------------------------------+
| hello                                         | Greet the assistant                            |
| help                                          | Show this help message                         |
| close / exit                                  | Exit the assistant                             |
+-----------------------------------------------+------------------------------------------------+
| CONTACTS                                                                                       |
+-----------------------------------------------+------------------------------------------------+
| add-contact <name> <phone>                    | Add a new contact                              |
| change-contact <name> <old_phone> <new_phone> | Change phone number                            |
| show-phone <name>                             | Show phone number(s)                           |
| all-contacts                                  | Display all contacts                           |
| add-birthday <name> <DD.MM.YYYY>              | Add birthday                                   |
| show-birthday <name>                          | Show birthday                                  |
| birthdays <days>                              | Upcoming birthdays                             |
| add-email <name> <email>                      | Add email to contact                           |
| edit-email <name> <new_email>                 | Update existing email                          |
| add-address <name> <address>                  | Add address to contact                         |
| edit-address <name> <new_address>             | Update existing address                       |
| search-contacts <field> <query>               | Search by: name, phone, email, address, all    |
| delete-contact <name>                         | Delete a contact                               |
+-----------------------------------------------+------------------------------------------------+
| NOTES                                                                                          |
+-----------------------------------------------+------------------------------------------------+
| add-note <title> <text>                       | Add a new note                                 |
| all-notes                                     | Display all notes                              |
| find-note <keyword>                           | Search notes by keyword                        |
| change-note <title> <new_text>                | Edit a note                                    |
| delete-note <title>                           | Delete a note                                  |
| add-tag <title> <tag>                         | Add a tag to a note                            |
| find-notes <tag>                              | Find notes by tag                              |
| all-tags                                      | Show all tags                                  |
+-----------------------------------------------+------------------------------------------------+
"""
