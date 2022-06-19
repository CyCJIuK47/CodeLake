import tkinter as tk

from tkinter import StringVar
from tkinter import filedialog


class PathSelector:
	def __init__(self, root, text, default_path):
		self.__text = text
		self.__selected_path = default_path

		self.__root = tk.LabelFrame(root, font=("TkFixedFont"))
		self.__label_text = StringVar(value=f"{self.__text}: {self.__selected_path}")

		self.__path_placeholder = tk.Label(self.__root, textvariable=self.__label_text,
	 										font=("TkFixedFont"), relief=tk.SUNKEN)
		self.__select_btn = tk.Button(self.__root, text="Select", width=10,
	 									font=("TkFixedFont"), command=self.__select_path)


	def pack(self, **args):
		self.__root.pack(**args)
		self.__path_placeholder.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.__select_btn.pack(side=tk.RIGHT, padx=(1, 0), fill=tk.Y)

	def get(self):
		return self.__selected_path
		
	def __select_path(self):
		path = filedialog.askdirectory()

		if path is not str():
			self.__selected_path = path
			self.__label_text.set(f"{self.__text}: {self.__selected_path}")
