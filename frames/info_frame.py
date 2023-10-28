"""
Information frame containing its respective frame and canvas.
"""

import tkinter as tk
from enum import Enum
from typing import Optional

import frames
from utils.bridge import ServerBridge


class QueryResult(Enum):
    """Types of query results on the pass."""
    MARKED = 'marked'
    STAFF = 'staff'
    REVOKED = 'revoked'


class InfoFrame:
    """
    Information frame, displayed on the top-left of the window. Contains information about the pass and pass holder.
    """

    def __init__(
        self, parent: tk.Misc, bridge: ServerBridge, id_: int, name: str, phone_number: str, pass_type: str
    ):
        """
        Initialize the information frame.

        :param parent: Parent of the frame.
        :type parent: tk.Misc
        :param id_: Pass ID of the pass holder.
        :type id_: int
        :param name: Name of the pass holder.
        :type name: str
        :param phone_number: Phone number of the pass holder.
        :type phone_number: int
        :param pass_type: Pass type.
        :type pass_type: PassType
        """

        fg_color = 'white'
        bg_color = 'black'

        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)

        self.canvas = tk.Canvas(
            self.frame, width=self.frame.cget('width'), height=self.frame.cget('height'), bg=bg_color
        )

        self.bridge = bridge

        self.canvas.pack()

        self.id_label = tk.Label(
            self.canvas, text=f'ID: {id_}', font=frames.generate_font(), fg=fg_color, bg='grey',
            width=self.canvas.winfo_screenwidth(), height=3
        )

        self.name_label = tk.Label(
            self.canvas, text=f'Name: {name}', font=frames.generate_font(), fg=fg_color, bg=bg_color
        )

        self.phone_number_label = tk.Label(
            self.canvas, text=f'Phone Number: {phone_number}', font=frames.generate_font(), fg=fg_color, bg=bg_color
        )

        self.pass_type_label = tk.Label(
            self.canvas, text=f'Pass Type: {pass_type}', font=frames.generate_font(), fg=fg_color,
            bg=bg_color
        )

        self.id_label.place(relx=0.5, rely=0, anchor=tk.N)
        self.name_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.phone_number_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.pass_type_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.generate_pass_info_box()

    def set_data(
        self, id_: int, name: str, phone_number: str, pass_type: str
    ):
        self.id_label.config(text=id_)
        self.name_label.config(text=name)
        self.phone_number_label.config(text=phone_number)
        self.pass_type_label.config(text=pass_type)

    def generate_pass_info_box(self, result=None):
        canvas_width = int(self.canvas.cget('width'))
        canvas_height = int(self.canvas.cget('height'))

        width_padding = canvas_width // 10
        height_padding = canvas_height // 10

        box_color = 'grey'
        text_color = 'white'

        self.dialog_box = self.canvas.create_rectangle(
            width_padding * 2, canvas_height // 2 + height_padding * 2,
            canvas_width - width_padding * 2, canvas_height - height_padding,
            fill=box_color
        )

        if result is not None:
            text = f"{result['text']}\n{result['subtext']}"
        else:
            text = 'Waiting...'

        self.text_label = tk.Label(
            self.canvas, text=text, font=frames.generate_font(font_size=24), bg=box_color, fg=text_color
        )

        self.text_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def update_pass_info_box(self, qr_codes, status: Optional[str] = None):
        if len(qr_codes) == 0:
            return

        qr = qr_codes[0]

        data = qr.data.decode('utf-8')
        result = self.bridge.verify(data)

        if status is None:
            status_code = result['status']

            if status_code == 200:
                self.canvas.itemconfig(self.dialog_box, fill='green')
                self.text_label.config(bg='green')
            else:
                self.canvas.itemconfig(self.dialog_box, fill='red')
                self.text_label.config(bg='red')
        else:
            self.canvas.itemconfig(self.dialog_box, fill='yellow')
            self.text_label.config(bg='orange')

        self.text_label.config(text=result['text'])
