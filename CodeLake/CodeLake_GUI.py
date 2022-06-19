import os
import time
import threading

from tkinter import *
from tkinter import messagebox

from CodeLake_Kernel import CodeLake
from logger import Logger
from timer import Timer
from progressbar import Progressbar
from GUI import SettingsMenu, Settings, widgets


class CodeLake_GUI:

    def __init__(self):
        self.__root = Tk()
        self.__root.title("CodeLake")
        self.__root.geometry("410x500")
        self.__root.resizable(False, False)
        self.__nickname = StringVar(value="Put your nickname here")

        #default settings
        self.__settings = Settings(os.getcwd(), False, ["OK"])

    def __init_main_widgets(self):
    
        self.__CodeLake_lbl = Label(self.__root, text="CodeLake", width=55,
                                    relief="groove").place(x=10, y=15)

        self.__nickname_ntr = Entry(self.__root, width=38, bd=3, justify='center',
                                    textvariable=self.__nickname).place(x=10, y=53)

        self.__option_menu_btn = Button(self.__root, text="Settings", width=20,
                                    command=self.__init_option_menu).place(x=250, y=50)

        self.__run_btn = Button(self.__root, text="Run", width=55,
                                command=self.__run)
        self.__run_btn.place(x=8,y=85)

        self.__logger = Logger(self.__root, height=20, width=48, bd=2)
        self.__logger.place(x=10,y=120)

        self.__progress_bar = Progressbar(self.__root, orient='horizontal',
                                              mode='determinate', length=280)
        self.__progress_bar.place(x=10,y=460)

        self.__timer = Timer(self.__root, fg="#eee", bg="#333", width=13)
        self.__timer.place(x=300,y=460)

    
    def __init_option_menu(self):
        new_window = widgets.ModalWindow(self.__root, "Settings")
        settings_menu = SettingsMenu(new_window, self.__settings)
        settings_menu.pack(fill=BOTH, expand=True)

        new_window.on_closing(lambda: self.__settings.update(settings_menu.get()))
        

    def __log_entry_hello(self):
        
        self.__logger.log("    ____          _      _          _         ")                
        self.__logger.log("   / ___|___   __| | ___| |    __ _| | _____  ")
        self.__logger.log("  | |   / _ \ / _` |/ _ \ |   / _` | |/ / _ \ ")
        self.__logger.log("  | |__| (_) | (_| |  __/ |__| (_| |   <  __/ ")
        self.__logger.log("   \____\___/ \__,_|\___|_____\__,_|_|\_\___| ")
        self.__logger.log()

        self.__logger.log_header("Submission parser for codeforces.com", 2)
        self.__logger.log("")
    
    def __run(self):
        
        if not os.path.isdir(self.__settings.storage_path):
            messagebox.showwarning(title="Incorrect folder",
                                   message="Choose correct path to storage in Settings menu and try again")
            return   
        
        if self.__settings.active_filters == []:
            messagebox.showwarning(title="Empty filter list",
                                       message="Choose at least one verdict filter")
            return

        if not CodeLake.check_nickname_existence(self.__nickname.get()):
            messagebox.showwarning(title="Incorrect nickname",
                                       message="Nickname not found")
            return 

        self.__run_btn.configure(state='disabled')
        run_th = threading.Thread(target=CodeLake.parse,
                          args=(self.__nickname.get(), self.__settings.storage_path, self.__progress_bar,
                                self.__settings.active_filters, self.__settings.problem_statements_parsing,
                                self.__logger))

        pb_handler_th = threading.Thread(target=self.__progress_bar_handler)
        
        self.__timer.start()
        run_th.start()
        pb_handler_th.start()

    def __progress_bar_handler(self):
        while not self.__progress_bar.is_full():
            time.sleep(5)
        
        self.__logger.log(f"All submission for {self.__nickname.get()} sucessfully parsed", 2)
        messagebox.showinfo(title="Parsing sucessfully done",
                            message=f"All submission for {self.__nickname.get()} sucessfully parsed")
        self.__timer.stop()
        self.__progress_bar.emptify()
        self.__run_btn.configure(state='normal')

    def init(self):
        self.__init_main_widgets()
        self.__log_entry_hello()
        self.__root.mainloop()
