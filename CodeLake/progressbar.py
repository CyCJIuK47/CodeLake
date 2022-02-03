import tkinter as tk

from tkinter import ttk


class Progressbar:


    def __init__(self, root, divisions=100, **args):
        self.__total_divs = divisions
        self.__current_divs = 0

        self.__progressbar = ttk.Progressbar(root, **args)

    def add_divisions(self, divisions_num):
        self.__current_divs += divisions_num
        self.__update_progress()

    def set_divisions(self, divisions_num):
        self.__current_divs = divisions_num
        self.__update_progress()
        
    def set_total_divisions(self, divisions):
        self.__total_divs = divisions
        self.__update_progress()
        
    def is_full(self):
        if self.__current_divs == self.__total_divs:
            return True

        return False

    def emptify(self):
        self.__current_divs = 0
        self.__update_progress()    

    def fill(self):
        self.__current_divs = self.__total_divs
        self.__update_progress()  

    def __update_progress(self):
        current_progress = (self.__current_divs / self.__total_divs) * 100
        self.__progressbar["value"] = current_progress
        
    def place(self, **args):
        self.__progressbar.place(**args)
