"""Imports"""
import re
import json
from bot_pkg.decor import read_file_check, validate_two_args, validate_one_arg, \
                            check_contact_exists
import colorama
from colorama import Fore
colorama.init(autoreset=True)

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


if __name__ == "__main__":
    pass
