import tkinter as tk


class ModalWindow(tk.Toplevel):
    def __init__(self, root, title=str()):
        super().__init__(root)
        super().title(title)
        super().lift()
        super().grab_set()
        
        self.__on_closing_func = None
        super().wm_protocol("WM_DELETE_WINDOW", self.__on_closing)
        
    def on_closing(self, func):
        self.__on_closing_func = func
    
    def __on_closing(self):
        if self.__on_closing_func is not None:
            self.__on_closing_func()
        super().destroy()