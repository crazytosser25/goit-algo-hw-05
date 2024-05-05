"""imports"""
import re
import sys
from typing import Pattern, Match
from pathlib import Path
import colorama
from colorama import Fore
colorama.init(autoreset=True)


def parse_log_line(line: str) -> dict:
    pattern: Pattern[str] = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    parsed: Match[str] = re.search(pattern, line)
    if parsed:
        return {
            'date': parsed.group(1),
            'time': parsed.group(2),
            'level': parsed.group(3),
            'message': parsed.group(4)
        }

def load_logs(file_path: str) -> list:
    output = []
    try:
        with open (file_path, "r", encoding="utf-8") as log_file:
            lines: list = log_file.readlines()
            for line in lines:
                output.append(parse_log_line(line))
            return output
    except FileNotFoundError:
        print('File not found.')
        return False

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda line: line['level'].lower() == level, logs))

def count_logs_by_level(logs: list) -> dict:
    output = {}
    for line in logs:
        level = line.get('level')
        if level in output:
            output[level] += 1
        else:
            output[level] = 1

    return output

def display_log_counts(counts: dict) -> None:
    print(f"\n{Fore.YELLOW}{'Logging level'.ljust(20, ' ')}{Fore.WHITE}|{Fore.YELLOW}Quantity")
    print('_' * 20 + '|' + '_' * 10)
    for key in counts:
        print(f"{Fore.GREEN}{key.ljust(20, ' ')}{Fore.WHITE}|{Fore.CYAN}{str(counts[key]).rjust(3, ' ')}")

def display_log_by_level(level_log: dict, level: str) -> None:
    print(f"\nLog details for level {Fore.RED}{level.upper()}:")
    for line in level_log:
        print(f"{Fore.YELLOW}{line['date']} {Fore.WHITE}{line['time']} - {Fore.CYAN}{line['message']}")

def main():
    log_level = False
    try:
        file_path = Path(f'{sys.argv[1]}')

    except IndexError:
        print(f'{Fore.RED}No path to folder')
        return

    try:
        log_level = sys.argv[2].lower() if len(sys.argv) > 1 else False
    except IndexError:
        pass

    log = load_logs(file_path)
    if log:
        counted_log = count_logs_by_level(log)
        display_log_counts(counted_log)

    if log_level:
        filtered_log = filter_logs_by_level(log, log_level)
        display_log_by_level(filtered_log, log_level)


if __name__ == '__main__':
    main()
