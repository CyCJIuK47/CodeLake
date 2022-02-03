from tkinter import *
 

class Logger(Text):

    
    def __init__(self, root, **args):
        Text.__init__(self, root, args)
        self.configure(state='disabled')
        self.tag_configure("center", justify = 'center',
                           font=("Arial", 14))

     
    def log(self, data="", newlines=0):
        self.configure(state='normal')

        self.insert(END, f" {data}\n")
        self.insert(END, "\n" * newlines)
        self.see("end")

        self.configure(state='disabled')

    def log_header(self, data="", newlines=0):
        self.configure(state='normal')

        end_index = self.index('end')
        last_index = str(float(end_index))
        prelast_index = str(float(end_index) - 1)
        
        self.insert(END, f" {data}")
        self.insert(END, "\n" * (newlines))
        self.tag_add("center", prelast_index, last_index)
        self.see("end")
        
        self.configure(state='disabled')
