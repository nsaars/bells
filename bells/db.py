from platform import system as check_os
import requests
from datetime import datetime, date
from timetable import TimeTable
import os


def change_path(path: str):
    if check_os() == "Linux":
        return path.replace("\\", "/")


class DB:
    def __init__(self):
        self.__all_sounds = []
        self.__today_music = []
        self.__today_bells = []

        self.__today = datetime.today().date()
        self.__celebrations = [(date(self.__today.year, 12, 15), date(self.__today.year, 12, 30), "new_year"),
                               (date(self.__today.year, 1, 1), date(self.__today.year, 1, 15), "new_year"), ]

        self.__time_table = TimeTable()

        self.__last_db_refresh = 0

        self.get_today_sound()
        self.refresh_time_table()

    def refresh_time_table(self):
        time_table_mtime = os.stat("time_table.txt").st_mtime
        planned_mtime = os.stat("planned.txt").st_mtime
        last_file_refresh = max(time_table_mtime, planned_mtime)
        if self.__last_db_refresh < last_file_refresh:
            self.__time_table.refresh()
            self.__last_db_refresh = datetime.now().timestamp()
            print(f"DateBase was refreshed")

    def get_today_sound(self):
        for celebration in self.__celebrations:
            if celebration[0] <= self.__today <= celebration[1]:
                self.__today_music = [
                    (change_path(rf"{os.getcwd()}\sounds\music\celebrations\{celebration[2]}" + "\\") + path) for path
                    in
                    os.listdir(change_path(rf"{os.getcwd()}\sounds\music\celebrations\{celebration[2]}"))]

                self.__today_bells = [
                    (change_path(rf"{os.getcwd()}\sounds\bells\celebrations\{celebration[2]}" + "\\") + path) for path
                    in
                    os.listdir(change_path(rf"{os.getcwd()}\sounds\bells\celebrations\{celebration[2]}"))]

                break
        else:
            self.__today_music = [(change_path(rf"{os.getcwd()}\sounds\music\default" + "\\") + path) for path in
                                  os.listdir(change_path(rf"{os.getcwd()}\sounds\music\default"))]
            self.__today_bells = [(change_path(rf"{os.getcwd()}\sounds\bells\default" + "\\") + path) for path in
                                  os.listdir(change_path(rf"{os.getcwd()}\sounds\bells\default"))]

    @staticmethod
    def world_time():
        time = datetime.strptime(
            requests.get("http://worldtimeapi.org/api/timezone/Europe/Moscow").json()['datetime'].split('.')[0],
            "%Y-%m-%dT%H:%M:%S")  # иногда сайт долго отвечает
        if (datetime.now() - time).seconds % 86340 > 59:
            print("Время на компьютере не совпадает с мировым!")
        return time

    def get_today_music(self):
        return self.__today_music

    def get_today_bells(self):
        return self.__today_bells

    def get_all_sounds(self):
        return self.__all_sounds

    def get_time_table(self):
        return self.__time_table.get_time_table()

    def today(self):
        return self.__today

    def get_celebrations(self):
        return self.__celebrations
