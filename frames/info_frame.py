"""
Information frame containing its respective frame and canvas.
"""

import tkinter as tk
from enum import Enum
from typing import Optional

import frames
from frames.pass_type import PassType


class QueryResult(Enum):
    """Types of query results on the pass."""
    VALID = 'valid'
    STAFF = 'staff'
    REVOKED = 'revoked'


class InfoFrame:
    """
    Information frame, displayed on the top-left of the window. Contains information about the pass and pass holder.
    """

    def __init__(
            self, parent: tk.Misc, id_: int, name: str, phone_number: int, pass_type: PassType,
            query_result: QueryResult, result_data: Optional[str] = None
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
        :param query_result: Query result on the pass.
        :type query_result: QueryResult
        :param result_data: Additional query result data, if required.
        :type result_data: Optional[str]
        """

        fg_color = 'white'
        bg_color = 'black'

        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)

        self.canvas = tk.Canvas(
            self.frame, width=self.frame.cget('width'), height=self.frame.cget('height'), bg=bg_color
        )

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
            self.canvas, text=f'Pass Type: {pass_type.value.title()}', font=frames.generate_font(), fg=fg_color,
            bg=bg_color
        )

        self.generate_pass_info_box(query_result, result_data)

        self.id_label.place(relx=0.5, rely=0, anchor=tk.N)
        self.name_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
        self.phone_number_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.pass_type_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    def generate_pass_info_box(self, query_result: QueryResult, result_data: Optional[str]):
        """
        Generate the information box with the pass query results.

        :param query_result: Query result on the pass.
        :type query_result: QueryResult
        :param result_data: Additional query data, if required.
        :type result_data: Optional[str]
        """

        canvas_width = int(self.canvas.cget('width'))
        canvas_height = int(self.canvas.cget('height'))

        width_padding = canvas_width // 10
        height_padding = canvas_height // 10

        box_color = self.canvas.cget('bg')
        text_color = 'white'

        match query_result:
            case QueryResult.VALID | QueryResult.STAFF:
                box_color = 'green'

            case QueryResult.REVOKED:
                box_color = 'red'

        self.canvas.create_rectangle(
            width_padding * 2, canvas_height // 2 + height_padding * 2,
            canvas_width - width_padding * 2, canvas_height - height_padding,
            fill=box_color
        )

        text = query_result.value.title()
        if query_result == QueryResult.REVOKED and result_data is not None:
            text += f'\n{result_data}'

        text_label = tk.Label(
            self.canvas, text=text, font=frames.generate_font(font_size=24), bg=box_color, fg=text_color
        )

        text_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
