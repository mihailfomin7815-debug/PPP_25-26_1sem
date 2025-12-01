import json
from datetime import datetime
import re


class Log:
    def __init__(self, level, time, msg):
        self.level = level
        self.time = time
        self.msg = msg
    def __str__(self):
        return f'[{self.time.strftime("%Y-%m-%d %H:%M:%S")}] {self.level} {self.msg}'

class LogFmt1:

    pat = re.compile(r'fmt1 \[(.+)\] (\w+): (.+)')

    @staticmethod
    def processing(inp):
        checking = LogFmt1.pat.match(inp)
        if checking:
            time1, level, msg = checking.groups()
            time2 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
            return Log(level, time2, msg)
        else:
            raise ValueError("Недопустимый формат лога fmt1")

class LogFmt2:

    pat = re.compile(r'fmt2 (\w+);(.+);(.+)')

    @staticmethod
    def processing(inp):
        checking = LogFmt2.pat.match(inp)
        if checking:
            level, time1, msg = checking.groups()
            time2 = datetime.strptime(time1, "%Y/%m/%d-%H:%M")
            return Log(level, time2, msg)
        else:
            raise ValueError("Недопустимый формат лога fmt2")

class LogJSON:

    @staticmethod
    def processing(inp):
        if inp[0:5] != 'json ':
            raise ValueError("Недопустимый формат лога json")
        jn = json.loads(inp[5:])
        keys = ("level", "time", "msg")
        if any(i not in jn for i in keys):
            raise ValueError("Недопустимый формат лога json")
        level, time1, msg = jn["level"], jn["time"], jn["msg"]
        time2 = datetime.strptime(time1, "%Y-%m-%dT%H:%M:%S")
        return Log(level, time2, msg)

class LogCommands:

    def __init__(self):
        self.records = []

    def record_add(self, record):
        self.records.append(record)

    def processing_inp(self, inp):
        for i in (LogFmt1, LogFmt2, LogJSON):
            try:
                log = i.processing(inp)
                self.record_add(log)
                print(f"Строка разобрана корректно")
                return
            except ValueError:
                continue
        print(f"Ошибка разбора строки: {inp}")

    def level_filter(self, level):
        return [r for r in self.records if r.level == level]

    def time_filter(self, start, end):
        return [r for r in self.records if start <= r.time <= end]

    def level_count(self, level: str):
        return f"Количество записей уровня {level}: {len(self.level_filter(level))}"

    def records_print(self, records=None):
        if records is None:
            records = self.records
        for r in records:
            print(r)

def process_commands(logs, command):
    parts = command.split()
    if parts[0] == "count" and parts[1][:6] == "level=":
        level = parts[1].split("=")[1]
        print(logs.level_count(level))
    elif parts[0] == "list" and parts[1][:6] == "level=":
        level = parts[1].split("=")[1]
        filt = logs.level_filter(level)
        print(f'Записи с уровнем {level}:')
        logs.records_print(filt)
    elif parts[0] == "range":
        start_str = parts[1] + " " + parts[2]
        end_str = parts[3] + " " + parts[4]
        start = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end = datetime.strptime(end_str, "%Y-%m-%d %H:%M")
        filt = logs.time_filter(start, end)
        print(f'Все записи с {start} по {end}:')
        logs.records_print(filt)
    else:
        print(f"Неизвестная команда: {command}")

lines = [
    "fmt1 [2025-10-01 12:34:56] INFO: System started",
    "fmt2 ERROR;2025/10/01-12:35;Disk full",
    'json {"level": "WARNING", "time": "2025-10-01T12:36:00", "msg": "High load"}',
    "bad log line"
]

logs = LogCommands()
for line in lines:
    logs.processing_inp(line)

print("Все записи:")
logs.records_print()

print("\nКоманды:")
process_commands(logs, "count level=ERROR")
process_commands(logs, "list level=WARNING")
process_commands(logs, "range 2025-10-01 12:30 2025-10-01 13:00")
