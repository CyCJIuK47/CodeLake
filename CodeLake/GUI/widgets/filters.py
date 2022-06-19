import tkinter as tk
from tkinter import ttk


class Filter:
    def __init__(self, root, name):
        self.name = name
        self.__frame = tk.Frame(root)
        self.__filter_state = tk.StringVar()
        self.__check_button = tk.Checkbutton(self.__frame, variable=self.__filter_state,
                                            onvalue=str(name), offvalue=str(), text=str(name),
                                            font=("TkFixedFont"))
    
    def pack(self, **args):
        self.__frame.pack(**args)
        self.__check_button.pack(side=tk.LEFT, fill=tk.X)

    def get(self):
        return self.__filter_state.get()
    
    def activate(self):
        self.__filter_state.set(str(self.name))
    
    def deactivate(self):
        self.__filter_state.set(str())


class FilterBox:
    def __init__(self, root, box_name, filters, active_filters=[]):
        self.__filters = filters
        self.__frame = tk.LabelFrame(root, text=box_name, font=("TkFixedFont"))
        self.__left_side = tk.Frame(self.__frame)
        self.__right_side = tk.Frame(self.__frame)

        left_filters, right_filters = self.__half_split(self.__filters)
        self.__filter_buttons = [Filter(self.__left_side, filter_) for filter_ in left_filters]
        self.__filter_buttons.extend([Filter(self.__right_side, filter_) for filter_ in right_filters])

        self.activate_filters(active_filters)
    
    def pack(self, **args):
        self.__frame.pack(**args)
        self.__left_side.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.__right_side.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        ttk.Separator(self.__frame, orient="vertical").pack(fill=tk.Y, side=tk.LEFT, pady=(5, 5))
        
        for filter_button in self.__filter_buttons:
            filter_button.pack(fill=tk.BOTH, expand=True, padx=(5, 5))

    def get_filters(self):
        return self.__filter_buttons
    
    def get_active_filters(self):
        return list(filter(lambda filter: filter.get() is not str(), self.__filter_buttons))
    
    def activate_filters(self, filters):
        for filter in self.__filter_buttons:
            if filter.name in filters:
                filter.activate()

    def deactivate_filters(self, filters):
        for filter in self.__filter_buttons:
            if filter.name in filters:
                filter.deactivate()

    def __half_split(self, iterable):
        return iterable[:len(iterable)//2], iterable[len(iterable)//2:]