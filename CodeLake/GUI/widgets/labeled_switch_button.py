import tkinter as tk

from switch_button import SwitchButton


class LabeledSwitchButton:
    def __init__(self, root, text, state=False):
        self.__frame = tk.LabelFrame(root)
        self.__label = tk.Label(self.__frame, text=text, font=("TkFixedFont"))
        self.__switch_button = SwitchButton(self.__frame, state)

    def pack(self, **args):
        self.__frame.pack(**args)
        self.__label.pack(side=tk.LEFT, fill=tk.X)
        self.__switch_button.pack(side=tk.RIGHT, fill=tk.X, padx=(10, 0))
    
    def get(self):
        return self.__switch_button.get()