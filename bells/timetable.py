from datetime import datetime
import os
import re


class TimeTable:
    def __init__(self):
        self.__time_table = []

    def refresh(self):
        with open("time_table.txt", "r", encoding='utf-8') as time_table:
            time_table_text = re.sub(r'\"', "", time_table.read().rstrip())
            for event in time_table_text.split('\n'):
                if event:
                    event = event.split()
                    event_dict = dict()
                    event_dict['done'] = False
                    event_dict['time'] = event[0]
                    event_dict['type'] = event[1]
                    event_dict['file_path'] = ''
                    if len(event) > 2:
                        if not os.path.exists(event[2]):
                            print(f'There is not such file {event[2]}')
                        else:
                            event_dict['file_path'] = event[2]
                    self.__time_table.append(event_dict)
        with open("planned.txt", "r", encoding='utf-8') as time_table:
            time_table_text = re.sub(r'\"', "", time_table.read().rstrip())
            for event in time_table_text.split('\n'):
                if event and datetime.strptime(event.split()[0], "%d/%m/%y").date() == datetime.today().date():
                    event = event.split()
                    event_dict = dict()
                    event_dict['done'] = False
                    event_dict['time'] = event[1]
                    event_dict['type'] = event[2]
                    event_dict['file_path'] = ''
                    if len(event) > 3:
                        if not os.path.exists(event[3]):
                            print(f'There is not such file {event[3]}')
                        else:
                            event_dict['file_path'] = event[3]
                    self.__time_table.append(event_dict)

        self.__time_table.sort(key=lambda x: (x['time'], -len(x)))
        return self.__time_table

    def get_time_table(self):
        return self.__time_table

