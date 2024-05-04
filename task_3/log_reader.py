"""imports"""
import re
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
    file: str = Path(file_path)
    output = []
    with open (file, "r", encoding="utf-8") as log_file:
        lines: list = log_file.readlines()
        for line in lines:
            output.append(parse_log_line(line))
        return output

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda line: line['level'].lower() == level, logs))

def count_logs_by_level(logs: list, level: str) -> dict:
    output: list = filter_logs_by_level(logs, level)
    return len(output)

def display_log_counts(counts: dict):
    print(f"{Fore.GREEN}{name.ljust(30, '.')}{Fore.CYAN}{phone}\n")

def main():
    pass


if __name__ == '__main__':
    log = load_logs('E:/Works/GoIT/goit-algo-hw-05/task_3/log.txt')
    test_lvl = count_logs_by_level(log, 'debug')
    print(test_lvl)
