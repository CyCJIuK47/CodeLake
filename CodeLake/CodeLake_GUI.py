import os
import time
import threading

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

from CodeLake_Kernel import CodeLake
from logger import Logger
from timer import Timer
from progressbar import Progressbar


class CodeLake_GUI:

    def __init__(self):
        self.__root = Tk()
        self.__root.title("CodeLake")
        self.__root.geometry("410x500")
        self.__root.resizable(False, False)

        self.__nickname = StringVar(value="Put your nickname here")
        self.__parse_problem_statement = BooleanVar(value=False)
        self.__path_to_dump = StringVar()

        self.__filters = [StringVar() for i in CodeLake.filters]
        self.__filters[0].set(CodeLake.filters[0])

    def __init_main_widgets(self):
    
        self.__CodeLake_lbl = Label(self.__root, text="CodeLake", width=55,
                                    relief="groove").place(x=10, y=15)

        self.__nickname_ntr = Entry(self.__root, width=38, bd=3, justify='center',
                                    textvariable=self.__nickname).place(x=10, y=53)

        self.__option_menu_btn = Button(self.__root, text="Options", width=20,
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

        option_menu = Toplevel(self.__root)
        option_menu.title("CodeLake")
        option_menu.geometry("415x500")
        option_menu.resizable(False, False)

        CodeLake_lbl = Label(option_menu, text="CodeLake",
                                     width=56, relief="groove").place(x=10,y=15)
 
        select_folder_btn = Button(option_menu, text ="Choose folder",
                                          width=19, command=self.__select_folder).place(x=265,y=57)

        chosen_folder_lbl = Label(option_menu, textvariable=self.__path_to_dump,
                                         width=35, relief="groove").place(x=10,y=60)

        self.__parse_problem_statement_lbl = Label(option_menu, text="Parse problem statements?",
                                                   width=56, relief="groove").place(x=10,y=100)

        parse_problem_statement_y = Radiobutton(option_menu, text='Yes', relief="groove", width=24,
                                                       variable=self.__parse_problem_statement, value=True).place(x=10,y=130)
        parse_problem_statement_n = Radiobutton(option_menu, text='No', relief="groove", width=24,
                                                       variable=self.__parse_problem_statement, value=False).place(x=212,y=130)

        filters_lbl = Label(option_menu, text="Verdict filters",
                                   relief="groove",width=56).place(x=10,y=170)
    
        filters_checkbuttons = []
        for i in range(0, len(self.__filters)):
            filters_checkbuttons.append(Checkbutton(option_menu, text=CodeLake.filters[i], variable=self.__filters[i],
                                                           onvalue=CodeLake.filters[i], offvalue=""))
    
        for i in range(0, len(filters_checkbuttons)):
            d_x = (i%2)*215
            d_y = (i//2)*30
            filters_checkbuttons[i].place(x=20+d_x, y=210+d_y)

    def __log_entry_hello(self):
        
        self.__logger.log("    ____          _      _          _         ")                
        self.__logger.log("   / ___|___   __| | ___| |    __ _| | _____  ")
        self.__logger.log("  | |   / _ \ / _` |/ _ \ |   / _` | |/ / _ \ ")
        self.__logger.log("  | |__| (_) | (_| |  __/ |__| (_| |   <  __/ ")
        self.__logger.log("   \____\___/ \__,_|\___|_____\__,_|_|\_\___| ")
        self.__logger.log()

        self.__logger.log_header("Submission parser for codeforces.com", 2)
        self.__logger.log("")
        
    
    def __select_folder(self):
        folder = filedialog.askdirectory()
        if folder!="":
            self.__path_to_dump.set(folder)
    
    def __run(self):
        
        if not os.path.isdir(self.__path_to_dump.get()):
            messagebox.showwarning(title="Incorrect folder",
                                   message="Choose folder in Options menu and try again")
            return   

        filters = [i.get() for i in self.__filters if i.get() != '']
        
        if filters == []:
            messagebox.showwarning(title="Empty verdict list",
                                       message="Choose at least one verdict")
            return

        if not CodeLake.check_nickname_existence(self.__nickname.get()):
            messagebox.showwarning(title="Incorrect nickname",
                                       message="Nickname not found")
            return 

        self.__run_btn.configure(state='disabled')
        run_th = threading.Thread(target=CodeLake.parse,
                          args=(self.__nickname.get(), self.__path_to_dump.get(), self.__progress_bar,
                                filters, self.__parse_problem_statement.get(), self.__logger))

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
