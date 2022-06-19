import tkinter as tk


class AnnotatedEntry:
    def __init__(self, root, annotation):
        self.__annotation = annotation
        self.__covertext = tk.StringVar(value=self.__annotation)
        self.__textvariable = tk.StringVar(value=str())
        self.__entry = tk.Entry(root, textvariable=self.__covertext, fg="gray",
                                justify=tk.CENTER, font=("TkFixedFont"))
        
        self.__entry.bind("<FocusIn>", self.__on_focus_in)
        self.__entry.bind("<FocusOut>", self.__on_focus_out)
    
    def pack(self):
        self.__entry.pack()
    
    def get(self):
        return self.__textvariable.get()
    
    def __on_focus_in(self, event):
        self.__entry.configure(fg="black")
        if self.__textvariable.get() is str():
            self.__covertext.set(str())

    def __on_focus_out(self, event):
        if self.__covertext is not str():
            self.__textvariable.set(self.__covertext.get())
            self.__entry.configure(fg="black")
        
        if self.__textvariable.get() is str():
            self.__covertext.set(self.__annotation)
            self.__entry.configure(fg="gray")