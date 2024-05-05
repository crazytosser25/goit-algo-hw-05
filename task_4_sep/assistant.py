"""Imports"""
from pathlib import Path
from bot_pkg import parse_input, read_file, write_file, add_contact, \
                            change_contact, delete_contact, show_phone, \
                            show_all, mistaken_arg, commands_help
import colorama
from colorama import Fore
colorama.init(autoreset=True)

def main():
    """This code is designed to create a simple command-line interface (CLI)
    application that interacts with a contacts database. The user can perform
    actions such as adding, changing, and viewing contact information. The CLI
    uses the 'colorama' module to add colors to the output strings for better
    readability.
    """
    database = Path("bot_pkg/contacts.json")
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
                print(commands_help())
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
