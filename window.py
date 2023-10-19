"""
Core window.
"""
import tkinter as tk
from enum import IntEnum

from PIL import Image
from PIL.ImageTk import PhotoImage


class FrameType(IntEnum):
    """
    Enum to retrieve the frame each corner of the display.
    """
    VIDEO = 1
    QR_CODE = 2
    FOO = 3
    BAR = 4


class Display:
    """
    Main display class. It composes the tk.Tk() and its corresponding canvas and frame children.
    """

    def __init__(self, title: str, full_screen: bool):
        """
        Initialise the display but not run it.

        :param title: Title of the tkinter display.
        :type title: str

        :param full_screen: Whether the display is fullscreen or "maximised". It is not truly maximised, just scaled to the display size.
        :type full_screen: bool
        """

        self._root = tk.Tk()
        self._root.title(title)

        if full_screen:
            self._root.attributes('-fullscreen', True)
        else:
            self._root.state('zoomed')

        self.width = self._root.winfo_screenwidth()
        self.height = self._root.winfo_screenheight()

        # Canvas is the code child of the root. It is to be modified and never the root directly.
        self._canvas = tk.Canvas(self._root, width=self.width, height=self.height, bg='white')
        self._canvas.pack()

        qr_code_image = Image.open('image.jpeg')
        self._init_frames(qr_code_image)

    def _init_frames(self, image: Image) -> dict[FrameType, tk.Frame]:
        """
        Initialize all four corner frames. Currently, contain three dummy frames and one image frame.

        :param image: Image to be loaded in the top-right frame.
        :type image: Image

        :return: All the four corner frames if required. Discard the return if not needed.
        :rtype: dict[FrameType, tk.Frame]
        """

        # Top-left frame to show incoming video streaming data.
        video_frame = tk.Frame(self._canvas, bg='red', width=self.width // 2, height=self.height // 2)
        video_label = tk.Label(video_frame, text='Video', fg='white', bg='red', font=('Helvetica', 48, 'bold'))
        video_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        photo_image = PhotoImage(image)

        # Top-right frame to hold an image.
        qr_code_frame = tk.Frame(self._canvas, width=self.width // 2, height=self.height // 2)
        qr_code_label = tk.Label(qr_code_frame, image=photo_image)
        qr_code_label.image = photo_image
        qr_code_label.pack(expand=True)

        # Bottom-right dummy frame.
        foo_frame = tk.Frame(self._canvas, bg='blue', width=self.width // 2, height=self.height // 2)
        foo_label = tk.Label(foo_frame, text='Foo', fg='white', bg='blue', font=('Helvetica', 48, 'bold'))
        foo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Bottom-left dummy frame.
        bar_frame = tk.Frame(self._canvas, bg='green', width=self.width // 2, height=self.height // 2)
        bar_label = tk.Label(bar_frame, text='Bar', fg='white', bg='green', font=('Helvetica', 48, 'bold'))
        bar_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._canvas.create_window(0, 0, anchor=tk.NW, window=video_frame)
        self._canvas.create_window(self.width // 2, 0, anchor=tk.NW, window=qr_code_frame)
        self._canvas.create_window(self.width // 2, self.height // 2, anchor=tk.NW, window=foo_frame)
        self._canvas.create_window(0, self.height // 2, anchor=tk.NW, window=bar_frame)

        return {
            FrameType.VIDEO: video_frame, FrameType.QR_CODE: qr_code_frame, FrameType.FOO: foo_frame,
            FrameType.BAR: bar_frame
        }

    def run(self):
        """
        Run the mainloop of the root.
        """
        self._root.mainloop()
