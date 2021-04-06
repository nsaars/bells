import pyaudio
import time


class Sound:
    def __init__(self):
        self.__py_audio = pyaudio.PyAudio()
        self.__name = ''
        self.__stop = False

    def play(self, wave_file, duration, name):
        self.__name = name

        def callback(in_data, frame_count, time_info, status):
            data = wave_file.readframes(frame_count)
            return data, pyaudio.paContinue

        stream = self.__py_audio.open(format=self.__py_audio.get_format_from_width(wave_file.getsampwidth()),
                                      channels=wave_file.getnchannels(),
                                      rate=wave_file.getframerate(),
                                      output=True,
                                      stream_callback=callback)

        stream.start_stream()
        while duration > 0 and stream.is_active() and not self.__stop:
            duration -= 1
            print(duration)
            time.sleep(1)
        stream.stop_stream()
        stream.close()
        wave_file.close()
        self.__stop = False

    def stop(self):
        self.__stop = True

    def get_name(self):
        return self.__name
