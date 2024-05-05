'''Imports'''
import re
import json
from pathlib import Path
import colorama
from colorama import Fore
colorama.init(autoreset=True)

# Decorators for errors check
def read_file_check(func) -> callable:
    """Decorator to handle file not found errors."""
    def inner(*args):
        try:
            return func(*args)
        except FileNotFoundError:
            return {}

    return inner

def validate_two_args(func):
    """Decorator to validate 2 contact arguments."""
    def inner(contacts, args):
        if len(args) != 2:
            return mistaken_arg('invalid args')
        _, phone = args
        if len(phone) not in [10, 13]:
            return mistaken_arg('invalid phone')
        return func(contacts, args)
    return inner

def validate_one_arg(func):
    """Decorator to validate 2 contact arguments."""
    def inner(contacts, args):
        if len(args) != 1:
            return mistaken_arg('no name for search')
        name = args[0]
        if name not in contacts:
            return mistaken_arg('phone not in contacts')
        return func(contacts, args)
    return inner

def check_contact_exists(func):
    """Decorator to check if the contact already exists."""
    def inner(contacts, args):
        name, _ = args
        if name in contacts:
            return mistaken_arg('contact exists')
        return func(contacts, args)
    return inner

# Functions
def parse_input(user_input: str) -> tuple:
    """Split the user's input into command and arguments.
        
    Args:
        user_input (str): User input string.

    Returns:
        tuple: A tuple containing the command and its arguments.
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    cmd = re.sub("[^A-Za-z]", "", cmd)
    return cmd, *args

@read_file_check
def read_file(database) -> dict:
    """Read and parse the contents of a JSON file containing contacts.
    
    Returns:
        dict: A dictionary representing the contacts with names as keys and phone numbers as values.
    """
    with open(database, "r", encoding="utf-8") as contacts_json:
        contacts_string = contacts_json.read()
        contacts_dict = json.loads(contacts_string)
    return contacts_dict

def write_file(database, contacts_dict: dict) -> None:
    """Writes the given dictionary of contacts to a JSON file named "contacts.json".

    Args:
        contacts_dict (dict): A dictionary representing the contacts, with
        names as keys and phone numbers as values.
    """
    contacts_string = json.dumps(contacts_dict, indent=2)
    with open(database, "w", encoding="utf-8") as contacts_json:
        contacts_json.write(contacts_string)

@validate_two_args
@check_contact_exists
def add_contact(contacts: dict, args: tuple) -> str:
    """Adds a new contact to the contacts dictionary based on user input.

    Args:
        contacts (dict): A dictionary containing contacts base.
        args (tuple): A tuple containing the name and phone number of the contact.

    Returns:
        str: A message indicating if the contact was added successfully.
    """
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@validate_two_args
def change_contact(contacts: dict, args: tuple) -> str:
    """Updates an existing contact in the contacts dictionary based on user input.

    Args:
        contacts (dict): A dictionary containing contacts base.
        args (tuple): A tuple containing the name and new phone number of the contact.

    Returns:
        str: A message indicating if the contact was updated successfully or not.
    """
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@validate_one_arg
def delete_contact(contacts: dict, args: tuple) -> str:
    """Deletes the contact from file.

    Args:
        contacts (dict): A dictionary containing contacts base.
        args (tuple): A tuple containing the name of the contact to delete.

    Returns:
        str: A message indicating if the contact was deleted successfully or not.
    """
    name = args[0]
    contacts.pop(name)
    return "Contact deleted."

@validate_one_arg
def show_phone(contacts: dict, args: tuple) -> str:
    """Displays the phone number of a contact based on user input.

    Args:
        contacts (dict): A dictionary containing contacts base.
        args (tuple): A tuple containing the name of the contact to search for.

    Returns:
        str: The phone number of the contact or an error message if the contact is not found.
    """
    name = args[0]
    return phone_line(name, contacts[name])

def show_all(contacts: dict) -> str:
    """Display all the contacts.

    Args:
        contacts (dict): A dictionary containing contacts base.

    Returns:
        str: The formatted list of contacts.
    """
    output_of_contacts: str = ''
    for name in contacts:
        output_of_contacts += phone_line(name, contacts[name])
    return output_of_contacts

def phone_line(name: str, phone: str) -> str:
    """Formats a contact's name and phone number into a displayable line.

    Args:
        name (str): The contact's name.
        phone (str): The contact's phone number.

    Returns:
        str: A formatted string containing the contact's name and phone number.
    """
    return f"{Fore.GREEN}{name.ljust(30, '.')}{Fore.CYAN}{phone}\n"

def mistaken_arg(mistake: str) -> str:
    """This function takes a single argument, `mistake` which is a string
    representing an error message. It returns a formatted string with colorful
    terminal output based on the given mistake.
    
    Args:
        mistake (str): The error message to be displayed.

    Returns:
        str: A formatted string containing the error message in colorful terminal output.
    """
    match mistake:
        case 'invalid command':
            return f"{Fore.RED}Invalid command."
        case 'phone not in contacts':
            return f"{Fore.RED}Invalid Name.\n{Fore.YELLOW}This contact doesn't exist."
        case 'contact exists':
            return f"{Fore.RED}Invalid Name.\n{Fore.YELLOW}This contact already exists."
        case 'no name for search':
            return f"{Fore.RED}Invalid data.\n{Fore.YELLOW}You must give me Name."
        case 'invalid phone':
            return f"{Fore.RED}Invalid Phone-number.\n{Fore.YELLOW}Must be 10 numbers, " \
                    "or 13 if in international format."
        case 'invalid args':
            return f"{Fore.RED}Invalid data.\n{Fore.YELLOW}You must give me Name and Phone-number."

def help_list() -> str:
    """Returns the list of commands.

    Returns:
        str: string with all commands
    """
    return "'close' or 'exit'\tto exit assistant.\n" \
            "'add [name] [phone]'\tto add new contact(phone must be 10 or 13 digits).\n" \
            "'change [name] [phone]'\tto change contact's phone number.\n" \
            "'del [name]'\t\tto delete contact from list.\n" \
            "'phone [name]'\t\tto review contact's phone number.\n" \
            "'all'\t\t\tto review all contacts.\n" 

# Main block
def main():
    """This code is designed to create a simple command-line interface (CLI)
    application that interacts with a contacts database. The user can perform
    actions such as adding, changing, and viewing contact information. The CLI
    uses the 'colorama' module to add colors to the output strings for better
    readability.
    """
    database = Path("contacts.json")
    contacts = read_file(database)
    print(f"\n{Fore.YELLOW}Welcome to the assistant bot!\n(enter 'help' for list of commands)\n")
    while True:
        user_input = input(f"Enter a command: {Fore.BLUE}")
        command, *args = parse_input(user_input)

        match command:
            case "close" | "exit":
                write_file(database, contacts)
                print(f"{Fore.YELLOW}Good bye!\n")
                break
            case "hello":
                print(f"{Fore.YELLOW}How can I help you?\n")
            case "help":
                print(help_list())
            case "add":
                print(f"{Fore.YELLOW}{add_contact(contacts, args)}\n")
            case "change":
                print(f"{Fore.YELLOW}{change_contact(contacts, args)}\n")
            case "del":
                print(f"{Fore.YELLOW}{delete_contact(contacts, args)}\n")
            case "phone":
                print(f"{show_phone(contacts, args)}\n")
            case "all":
                print(show_all(contacts))
            case _:
                print(f"{mistaken_arg('invalid command')}\n")


if __name__ == "__main__":
    main()
