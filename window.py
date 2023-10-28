"""
Core window.
"""
import tkinter as tk
from enum import IntEnum

import requests
from PIL import Image

from frames.admittance_frame import AdmittanceFrame
from frames.controls_frame import ControlsFrame
from frames.info_frame import InfoFrame
from frames.video_frame import VideoFrame
from utils.bridge import ServerBridge
from utils.video_capture import VideoCapture


class FrameType(IntEnum):
    """
    Enum to retrieve the frame each corner of the display.
    """
    VIDEO = 1
    INFO = 2
    FOO = 3
    BAR = 4


class Display:
    """
    Main display class. It composes the tk.Tk() and its corresponding canvas and frame children.
    """

    def __init__(self, title: str, full_screen: bool, kiosk_name: str, server_ip: str, assignment_name: str):
        """
        Initialise the display but not run it.

        :param title: Title of the tkinter display.
        :type title: str

        :param full_screen: Whether the display is fullscreen or "maximised". It is not truly maximised, just scaled to the display size.
        :type full_screen: bool
        """

        self.root = tk.Tk()
        self.root.title(title)

        if full_screen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.state('zoomed')

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.server_bridge = ServerBridge()

        # Canvas is the code child of the root. It is to be modified and never the root directly.
        self._canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self._canvas.pack()

        self.frames = self._init_frames()
        self._init_status_bar(kiosk_name, server_ip, assignment_name)

    def _init_frames(self, video_source: str = 'http://localhost:5000/video') -> dict[FrameType, tk.Frame]:
        """
        Initialize all four corner frames. Currently, contain three dummy frames and one image frame.

        :param image: Image to be loaded in the top-right frame.
        :type image: Image

        :return: All the four corner frames if required. Discard the return if not needed.
        :rtype: dict[FrameType, tk.Frame]
        """

        # Top-right frame to hold pass information.
        info_frame = InfoFrame(self._canvas, self.server_bridge, 123, "ABC", '---', '!STAFF!')

        # Bottom-right dummy frame.
        # foo_frame = tk.Frame(self._canvas, bg='blue', width=self.width // 2, height=self.height // 2)
        # foo_label = tk.Label(foo_frame, text='Foo', fg='white', bg='blue', font=('Helvetica', 48, 'bold'))
        # foo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.admittance_frame = AdmittanceFrame(self._canvas, self.server_bridge, info_frame)

        # Top-left frame to show incoming video streaming data.
        self.video_frame = VideoFrame(self._canvas, self.server_bridge, info_frame, self.admittance_frame)

        # Bottom-left dummy frame.
        bar_frame = ControlsFrame(self._canvas)
        # bar_frame = tk.Frame(self._canvas, bg='green', width=self.width // 2, height=self.height // 2)

        self._canvas.create_window(0, 0, anchor=tk.NW, window=self.video_frame.frame)
        self._canvas.create_window(self.width // 2, 0, anchor=tk.NW, window=info_frame.frame)
        self._canvas.create_window(self.width // 2, self.height // 2, anchor=tk.NW, window=self.admittance_frame.frame)
        self._canvas.create_window(0, self.height // 2, anchor=tk.NW, window=bar_frame.frame)

    def _init_status_bar(self, kiosk_name: str, server_ip: str, assignment_name: str):
        text = f'{kiosk_name.title()} enslaved to {server_ip.lower()} assigned to {assignment_name.title()}'

        status_bar_label = tk.Label(
            self._canvas, text=text, fg='white', bg='black', width=self._canvas.winfo_screenwidth()
        )
        status_bar_label.place(relx=0.5, rely=0, anchor=tk.N)

    def run(self):
        """
        Run the mainloop of the root.
        """
        self.root.mainloop()


def apply_video_stream(display_core: Display, capture: VideoCapture):
    image = display_core.video_frame.generate_image(capture)
    display_core.video_frame.refresh_image(image)

    display_core.root.after(1, lambda: apply_video_stream(display_core, capture))


if __name__ == '__main__':
    try:
        requests.get('https://www.google.com')
    except Exception as e:
        print(f'Connection Error: {e}')
        exit(1)

    bridge = ServerBridge()
    assignment = bridge.assignment

    if assignment is None:
        assignment_name = 'None'
    else:
        assignment_name = bridge.assignment.get('a_name', 'None')

    display = Display('Ticket Validation Kiosk', False, bridge.kiosk_name, bridge.server_ip, assignment_name)
    apply_video_stream(display, VideoCapture('http://localhost:5000/video'))
    display.run()
