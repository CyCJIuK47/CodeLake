import tkinter as tk


class SwitchButton:
    def __init__(self, root, state=False):
        self.__state = state
        self.__widget_params = {True: dict(padx=(15, 0), bg="green", text="On"),
                                False: dict(padx=(0, 15), bg="gray", text="Off")}

        self.__frame = tk.LabelFrame(root, bg=self.__widget_params[self.__state]["bg"])
        self.__button = tk.Button(self.__frame, width=8, font=("TkFixedFont"),
                                text=self.__widget_params[self.__state]["text"],
                                command=self.__switch)
    
    def pack(self, **args):
        self.__frame.pack(**args)
        self.__button.pack(fill=tk.X, padx=self.__widget_params[self.__state]["padx"])

    def get(self):
        return self.__state
    
    def __switch(self):
        self.__state = not self.__state
        
        self.__button.pack_forget()
        self.__frame.configure(bg=self.__widget_params[self.__state]["bg"])
        self.__button.configure(text=self.__widget_params[self.__state]["text"])
        self.__button.pack(fill=tk.X, padx=self.__widget_params[self.__state]["padx"])
