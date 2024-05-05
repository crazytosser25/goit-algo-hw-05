"""Imports"""
import colorama
from colorama import Fore
colorama.init(autoreset=True)

def mistaken_arg(mistake: str) -> str:
    """Colorized output in case of user input mistakes.
    This function takes a single argument, `mistake` which is a string
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

def commands_help() -> str:
    """Returns the list of commands for bot."""
    return "'add [name] [phone]'\tto add new contact(phone must be 10 or 13 digits).\n" \
            "'all'\t\t\tto review all contacts.\n" \
            "'change [name] [phone]'\tto change contact's phone number.\n" \
            "'del [name]'\t\tto delete contact from list.\n" \
            "'phone [name]'\t\tto review contact's phone number.\n" \
            "'close' or 'exit'\tto exit assistant.\n"


if __name__ == "__main__":
    pass
