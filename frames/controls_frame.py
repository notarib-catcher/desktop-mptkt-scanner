import socket
import tkinter as tk
from typing import Optional

from utils.bridge import ServerBridge
from frames import generate_font


class ControlsFrame:
    def __init__(self, parent: tk.Misc):
        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)
        self.canvas = tk.Canvas(self.frame, width=self.frame.cget('width'), height=self.frame.cget('height'))

        self.canvas.pack()

        self._post_init()
        self._init_form()

    def _post_init(self):
        internet_connection = self.is_connected_to_internet()

        if not internet_connection:
            tk.Label(self.canvas, text='Not connected to internet').place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

        self.server_bridge = ServerBridge()

        if not self.server_bridge.need_init:
            tk.Label(self.canvas, text='Initialization not required.').place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

        self._init_form()

    def _init_form(self):
        code_label = tk.Label(self.canvas, text='Code', font=generate_font(font_size=24))
        name_label = tk.Label(self.canvas, text='Name', font=generate_font(font_size=24))
        origin_label = tk.Label(self.canvas, text='Origin', font=generate_font(font_size=24))

        self.code_entry = tk.Entry(self.canvas, show='*', font=generate_font(font_size=24))
        self.name_entry = tk.Entry(self.canvas, font=generate_font(font_size=24))
        self.origin_entry = tk.Entry(self.canvas, font=generate_font(font_size=24))

        self.submit_button = tk.Button(self.canvas, text='Submit', font=generate_font(), command=self.submit_form_data)
        self.quit_button = tk.Button(self.canvas, text='Quit', font=generate_font(), command=self.canvas.quit)

        code_label.place(relx=0.35, rely=0.15, anchor=tk.E)
        self.code_entry.place(relx=0.45, rely=0.15, anchor=tk.W)

        name_label.place(relx=0.35, rely=0.3, anchor=tk.E)
        self.name_entry.place(relx=0.45, rely=0.3, anchor=tk.W)

        origin_label.place(relx=0.35, rely=0.45, anchor=tk.E)
        self.origin_entry.place(relx=0.45, rely=0.45, anchor=tk.W)

        self.quit_button.place(relx=0.35, rely=0.6, anchor=tk.CENTER)
        self.submit_button.place(relx=0.625, rely=0.6, anchor=tk.CENTER)

    def submit_form_data(self):
        error_label = tk.Label(self.canvas, text='Code should be an integer.', font=generate_font())
        code = self.code_entry.get()

        code_int: Optional[str] = None

        try:
            code_int = str(code)
        except ValueError:
            error_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        if code_int is not None:
            self.server_bridge.enroll(self.origin_entry.get(), code_int, self.name_entry.get())
            self.server_bridge.need_init = False

            if self.server_bridge.get_assignment():
                assignment = self.server_bridge.assignment
                print(assignment.get('a_id'))
                print(assignment.get('name'))

            else:
                print('No assignment found.')

            # TODO: Populate the assignment for the server bridge here.

    @staticmethod
    def is_connected_to_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 5) -> bool:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True

        except socket.error:
            return False
