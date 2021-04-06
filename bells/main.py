from db import DB
from sound import Sound
from poll import Poll
from datetime import datetime
from random import choice
from time import sleep
import wave
import os

sound = Sound()
db = DB()
poll = Poll()

poll.get_poll_results()


def main():
    db.refresh_time_table()

    for event in db.get_time_table():
        if event['done']:
            continue

        if datetime.now().strftime("%H:%M") in event['time']:
            if event['type'] == "bell":
                if event['file_path']:
                    bell = event['file_path']
                else:
                    bell = choice(db.get_today_bells())

                print(bell)
                wave_file = wave.open(bell, 'rb')
                sound.play(wave_file, 10, bell)
                event['done'] = True

            elif event['type'] == "music":
                f = datetime.strptime(event['time'].split(',')[1], "%H:%M")
                while datetime.now().strftime("%H:%M") != event['time'].split(',')[1]:
                    s = datetime.now()
                    if event['file_path']:
                        song = event['file_path']
                    else:
                        song = choice(db.get_today_music())

                    print(song)
                    wave_file = wave.open(song, 'rb')
                    sound.play(wave_file, (f - s).seconds, song)
                    event['done'] = True

            else:
                path = event['file_path']
                print(path)

                if os.path.exists(path):
                    wave_file = wave.open(event['file_path'], 'rb')
                    sound.play(wave_file, 999, path)
                    event['done'] = True
                else:
                    print(f"There is no such file {path}")


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as err:
            print(err)
        sleep(3)
