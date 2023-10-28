import tkinter as tk

import utils
from frames import generate_font
from frames.info_frame import InfoFrame
from utils.bridge import ServerBridge


class AdmittanceFrame:
    def __init__(self, parent: tk.Misc, bridge: ServerBridge, info_frame: InfoFrame):
        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)
        self.canvas = tk.Canvas(self.frame, width=self.frame.cget('width'), height=self.frame.cget('height'))

        self.bridge = bridge
        self.info_frame = info_frame
        self.qr = None

        self.canvas.pack()

        self._init_controls()

    def _init_controls(self):
        self.mark_attendance_button = tk.Button(
            self.canvas, text='Mark Attendance', font=generate_font(),
            command=self.mark_attendance
        )
        self.mark_attendance_button['state'] = 'disabled'

        self.invert_color_button = tk.Button(
            self.canvas, text='Invert Color', font=generate_font(),
            command=self.invert_color
        )

        self.mark_attendance_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.invert_color_button.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    def mark_attendance(self):
        if self.qr is None:
            return

        decode = self.qr.data.decode('utf-8')
        if self.bridge.mark_attendance(decode):
            self.info_frame.update_pass_info_box([self.qr], 'Marked')

    def invert_color(self):
        utils.INVERT_COLOR = not utils.INVERT_COLOR
