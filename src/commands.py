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
| all-contacts                                  | Display all contacts                           |
| delete-contact <name>                         | Delete a contact                               |
+-----------------------------------------------+------------------------------------------------+
| PHONE                                                                                          |
+-----------------------------------------------+------------------------------------------------+
| edit-contact <name> <old_phone> <new_phone>   | Change phone number                            |
| show-phone <name>                             | Show phone number(s)                           |
+-----------------------------------------------+------------------------------------------------+
| BIRTHDAY                                                                                       |
+-----------------------------------------------+------------------------------------------------+
| add-birthday <name> <DD.MM.YYYY>              | Add birthday                                   |
| show-birthday <name>                          | Show birthday                                  |
| birthdays <days>                              | Upcoming birthdays                             |
+-----------------------------------------------+------------------------------------------------+
| EMAIL                                                                                          |
+-----------------------------------------------+------------------------------------------------+
| add-email <name> <email>                      | Add email to contact                           |
| edit-email <name> <new_email>                 | Update existing email                          |
+-----------------------------------------------+------------------------------------------------+
| ADDRESS                                                                                        |
+-----------------------------------------------+------------------------------------------------+
| add-address <name> <address>                  | Add address to contact                         |
| edit-address <name> <new_address>             | Update existing address                        |
+-----------------------------------------------+------------------------------------------------+
| NOTES                                                                                          |
+-----------------------------------------------+------------------------------------------------+
| add-note <title> <content>                    | Add a new note                                 |
| all-notes                                     | Display all notes                              |
| find-note <field> <value>                     | Find notes: field = keyword or tag             |
| edit-note <title> <content>                   | Edit a note                                    |
| delete-note <title>                           | Delete a note                                  |
| add-tag <title> <tag>                         | Add a tag to a note                            |
| all-tags                                      | Show all tags                                  |
+-----------------------------------------------+------------------------------------------------+
"""
