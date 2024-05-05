"""Imports"""
from bot_pkg.colors import mistaken_arg

def read_file_check(func) -> callable:
    """Decorator to handle file not found errors."""
    def inner(*args):
        try:
            return func(*args)
        except FileNotFoundError:
            return {}

    return inner

def validate_two_args(func):
    """Decorator to validate functions with 2 arguments."""
    def inner(contacts, args):
        if len(args) != 2:
            return mistaken_arg('invalid args')
        _, phone = args
        if len(phone) not in [10, 13]:
            return mistaken_arg('invalid phone')
        return func(contacts, args)

    return inner

def validate_one_arg(func):
    """Decorator to validate functions with 1 argument."""
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


if __name__ == "__main__":
    pass
