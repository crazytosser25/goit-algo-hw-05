"""imports"""
import re
import sys
from typing import Match, List, Union
from pathlib import Path
import colorama
from colorama import Fore
colorama.init(autoreset=True)


def parse_log_line(line: str) -> dict:
    """Parse a log line and extract relevant information.

    This function takes a log line as input and extracts the date, time, log level,
    and message from it.
    It has the following keys:
        - 'date' (str): The date of the log entry in the format 'YYYY-MM-DD'.
        - 'time' (str): The time of the log entry in the format 'HH:MM:SS'.
        - 'level' (str): The log level indicating the severity ('INFO', 'ERROR').
        - 'message' (str): The log message containing the details of the event.

    Args:
        line (str): A single log line to be parsed.

    Returns:
        dict: A dictionary containing the parsed information.
    """
    pattern: str = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    parsed: Match[str] = re.search(pattern, line)
    if parsed:
        return {
            'date': parsed.group(1),
            'time': parsed.group(2),
            'level': parsed.group(3),
            'message': parsed.group(4)
        }

def load_logs(file_path: str) -> Union[List[dict], None]:
    """Load and parse log entries from a file.

    This function reads log entries from a specified file, parses each entry,
    and returns a list of dictionaries containing the parsed information.
    Note:
        This function relies on the `parse_log_line` function to parse individual log lines.

    Args:
        file_path (str): The path to the log file to be loaded and parsed.

    Returns:
        Union[List[dict], None]: A list of dictionaries representing the parsed log entries,
        or None if there was an error during file processing or if the log data has incorrect
        format.
        
    """
    output = []
    try:
        with open (file_path, "r", encoding="utf-8") as log_file:
            lines: list = log_file.readlines()
            for line in lines:
                parsed_line = parse_log_line(line)
                if parsed_line:
                    output.append(parsed_line)
                else:
                    print(f'{Fore.RED}Wrong data format.')
                    return None
            return output
    except FileNotFoundError:
        print(f'{Fore.RED}File not found.')
        return None

def filter_logs_by_level(logs: list, level: str) -> list:
    """Filter log entries by log level.

    This function takes a list of log entries and filters them based on the specified log level.
    The log level comparison is case-insensitive.

    Args:
        logs (list): A list of dictionaries representing log entries.
        level (str): The log level to filter by. Case-insensitive.

    Returns:
        list: A list of log entries matching the specified log level.
    """
    return list(filter(lambda line: line['level'].lower() == level, logs))

def count_logs_by_level(logs: list) -> dict:
    """Count the occurrences of each log level in a list of log entries.

    This function takes a list of log entries and counts the occurrences of each log level.

    Args:
        logs (list): A list of dictionaries representing log entries.

    Returns:
        dict: A dictionary where keys are log levels and values are the counts
            of occurrences of each log level in the input list of log entries.
    """
    output = {}
    for line in logs:
        level = line.get('level')
        if level in output:
            output[level] += 1
        else:
            output[level] = 1

    return output

def display_log_counts(counts: dict) -> None:
    """Display log level counts in a tabular format.

    This function takes a dictionary containing log level counts and displays them in
    a tabular format.
    Note:
        - The function prints the log level counts in a formatted table.
        - It uses Colorama for colored output.

    Args:
        counts (dict): A dictionary where keys are log levels and values are the counts
                        of occurrences of each log level.
    """
    # Header
    print(
        f"\n{Fore.YELLOW}{'Logging level'.ljust(20, ' ')}{Fore.WHITE}|"
        f"{Fore.YELLOW}Quantity"
    )
    print('_' * 20 + '|' + '_' * 10)
    # Lines of table
    for key in counts:
        print(
            f"{Fore.GREEN}{key.ljust(20, ' ')}{Fore.WHITE}|"
            f"{Fore.CYAN}{str(counts[key]).rjust(3, ' ')}"
        )

def display_log_by_level(level_log: dict, level: str) -> None:
    """Display log details for a specific log level.

    This function takes a dictionary containing log entries and displays log details
    for a specific log level in a formatted manner.
    Note:
        - The function prints date, time, and message.
        - It uses Colorama for colored output.

    Args:
        level_log (dict): A dictionary containing log entries, where each entry is represented
                            as a dictionary with keys: 'date', 'time', 'level', and 'message'.
        level (str): The log level for which log details are to be displayed.
    """
    print(f"\nLog details for level {Fore.RED}{level.upper()}:")
    for line in level_log:
        print(
            f"{Fore.YELLOW}{line['date']} {Fore.WHITE}{line['time']} "
            f"- {Fore.CYAN}{line['message']}"
        )

def main():
    """
    This function serves as the entry point of the program. It loads log data
    from a specified file, displays statistics about log levels, and optionally
    displays log details for a specific log level.

    """
    log_level = False
    # Trying if path to file is present
    try:
        file_path = Path(f'{sys.argv[1]}')

    except IndexError:
        print(f'{Fore.RED}No path to folder')
        return
    # Trying if log level arg is present
    try:
        log_level = sys.argv[2].lower() if (len(sys.argv) > 1) else False
    except IndexError:
        pass
    # parsing pile
    log = load_logs(file_path)
    # Displaying statistic
    if log:
        display_log_counts(count_logs_by_level(log))
    # Displaying details
    if log_level:
        display_log_by_level(filter_logs_by_level(log, log_level), log_level)


if __name__ == '__main__':
    main()
