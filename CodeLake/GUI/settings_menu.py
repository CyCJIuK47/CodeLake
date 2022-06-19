import tkinter as tk

from filterlist import filters
from widgets import PathSelector, FilterBox, LabeledSwitchButton


class Settings:
    def __init__(self, storage_path, problem_statements_parsing, active_filters):
        self.storage_path = storage_path
        self.problem_statements_parsing = problem_statements_parsing
        self.active_filters = active_filters
    
    def update(self, settings):
        self.storage_path = settings.storage_path
        self.problem_statements_parsing = settings.problem_statements_parsing
        self.active_filters = settings.active_filters


class SettingsMenu:
    def __init__(self, root, settings):
        self.__root = root
        self.__frame = tk.Frame(self.__root)
        self.__path_selector = PathSelector(self.__frame, "Storage Path", settings.storage_path)
        self.__switch_button = LabeledSwitchButton(self.__frame, "Problem statements parsing",
                                                    settings.problem_statements_parsing)
        self.__filter_box = FilterBox(self.__frame, "Filters", filters, settings.active_filters)

    def pack(self, **args):
        self.__frame.pack(padx=(5, 5), pady=(5, 5), **args)
        self.__path_selector.pack(fill=tk.X, pady=(5, 5))
        self.__switch_button.pack(fill=tk.X, pady=(5, 5))
        self.__filter_box.pack(fill=tk.BOTH, expand=True)

    def get(self):
        return Settings(self.__path_selector.get(), self.__switch_button.get(),
                        [filter.get() for filter in self.__filter_box.get_active_filters()])