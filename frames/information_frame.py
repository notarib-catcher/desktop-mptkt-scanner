import tkinter as tk

import frames
from utils.bridge import ServerBridge


class InformationFrame:
    def __init__(self, parent: tk.Misc, bridge: ServerBridge):
        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)
        self.canvas = tk.Canvas(self.frame, width=self.frame.cget('width'), height=self.frame.cget('height'))

        self.bridge = bridge

        self.canvas.pack()

        self._init_ui()

    def _init_ui(self):
        self.id_label = tk.Label(
            self.canvas, text='', font=frames.generate_font(), width=self.canvas.winfo_screenwidth(), height=3
        )

        self.name_label = tk.Label(self.canvas, text='', font=frames.generate_font())

        self.phone_number_label = tk.Label(self.canvas, text='', font=frames.generate_font())

        self.id_label.place(relx=0.5, rely=0, anchor=tk.N)
        self.name_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.phone_number_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

    def update_ui_data(self, id_: int, name: str, phone_number: str):
        self.id_label.config(text=f'ID: {id_}')
        self.name_label.config(text=f'Name: {name}')
        self.phone_number_label.config(text=f'Phone Number: {phone_number}')
