import time
import threading
import tkinter as tk

from tkinter import StringVar


class Timer(tk.Label):


    def __init__(self, root, **args):

        self.__total_seconds = 0
        self.__is_running = False
        self.__timer_label = StringVar(value="00:00:00")
        tk.Label.__init__(self, root, args,
                          textvariable=self.__timer_label)

    def __clock(self):
        self.__total_secons = 0
        self.__is_running = True

        while self.__is_running:
            time.sleep(1)
            self.__total_seconds += 1
            self.__timer_label.set(self.__time_to_string())

    def start(self):
        clock_process = threading.Thread(target=self.__clock)
        clock_process.start()

    def stop(self):
        self.__is_running = False
        time.sleep(1)

        self.__total_seconds = 0
        self.__timer_label.set("00:00:00")

    def __time_to_string(self):
        
        hours = str(self.__total_seconds // 3600)
        minutes = str((self.__total_seconds % 3600) // 60)
        seconds = str(self.__total_seconds % 60)

        ## add leading zeros
        if len(hours) == 1:
            hours = "0" + hours
        if len(minutes) == 1:
            minutes = "0" + minutes
        if len(seconds) == 1:
            seconds = "0" + seconds

        return f"{hours}:{minutes}:{seconds}"
