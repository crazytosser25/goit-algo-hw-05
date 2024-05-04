from typing import Pattern, Match
import re
from pathlib import Path

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
    file = Path(file_path)
    with open (file, "r", encoding="utf-8") as log_file:
        lines: list = log_file.readlines()
        for line in lines:
            parse_log_line(line)
        return lines

def filter_logs_by_level(logs: list, level: str) -> list:
    pass

def count_logs_by_level(logs: list) -> dict:
    pass

def display_log_counts(counts: dict):
    pass

def main():
    pass


if __name__ == '__main__':
    print(load_logs('E:/Works/GoIT/goit-algo-hw-05/task_3/log.txt'))

    # file_address, *args = line.split()
    # args = args.strip().lower()    
    # return file_address, *args