"""
Core window.
"""
import tkinter as tk
from enum import IntEnum

from PIL import Image
from PIL.ImageTk import PhotoImage

from frames.info_frame import InfoFrame, QueryResult
from frames.pass_type import PassType


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
        self._canvas = tk.Canvas(self._root, width=self.width, height=self.height, bg='black')
        self._canvas.pack()

        video_frame_image = Image.open('assets/image.jpeg')
        self._init_frames(video_frame_image)

    def _init_frames(self, image: Image) -> dict[FrameType, tk.Frame]:
        """
        Initialize all four corner frames. Currently, contain three dummy frames and one image frame.

        :param image: Image to be loaded in the top-right frame.
        :type image: Image

        :return: All the four corner frames if required. Discard the return if not needed.
        :rtype: dict[FrameType, tk.Frame]
        """

        # Top-left frame to show incoming video streaming data.
        photo_image = PhotoImage(image)

        video_frame = tk.Frame(self._canvas, bg='red', width=self.width // 2, height=self.height // 2)
        video_label = tk.Label(video_frame, image=photo_image)
        video_label.image = photo_image
        video_label.pack(expand=True)

        # Top-right frame to hold pass information.
        info_frame = InfoFrame(
            self._canvas, 123, 'ABC', 123, PassType.E_SPORTS, QueryResult.REVOKED,
            'Lorem ipsum dolor si amet.'
        )

        # Bottom-right dummy frame.
        foo_frame = tk.Frame(self._canvas, bg='blue', width=self.width // 2, height=self.height // 2)
        foo_label = tk.Label(foo_frame, text='Foo', fg='white', bg='blue', font=('Helvetica', 48, 'bold'))
        foo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Bottom-left dummy frame.
        bar_frame = tk.Frame(self._canvas, bg='green', width=self.width // 2, height=self.height // 2)
        bar_label = tk.Label(bar_frame, text='Bar', fg='white', bg='green', font=('Helvetica', 48, 'bold'))
        bar_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self._canvas.create_window(0, 0, anchor=tk.NW, window=video_frame)
        self._canvas.create_window(self.width // 2, 0, anchor=tk.NW, window=info_frame.frame)
        self._canvas.create_window(self.width // 2, self.height // 2, anchor=tk.NW, window=foo_frame)
        self._canvas.create_window(0, self.height // 2, anchor=tk.NW, window=bar_frame)

        return {
            FrameType.VIDEO: video_frame, FrameType.INFO: info_frame, FrameType.FOO: foo_frame,
            FrameType.BAR: bar_frame
        }

    def run(self):
        """
        Run the mainloop of the root.
        """
        self._root.mainloop()


if __name__ == '__main__':
    display = Display('Ticket Validation Kiosk', True)
    display.run()
