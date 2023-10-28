import tkinter as tk
from ctypes import windll
from typing import Optional

import cv2
from PIL import Image
from PIL.ImageTk import PhotoImage

import utils
from frames.admittance_frame import AdmittanceFrame
from frames.info_frame import InfoFrame
from utils import decode_qr, get_buffer_and_qr_codes
from utils.bridge import ServerBridge
from utils.video_capture import VideoCapture


class VideoFrame:
    def __init__(self, parent: tk.Misc, bridge: ServerBridge, info_frame: InfoFrame, admittance_frame: AdmittanceFrame):
        self.frame = tk.Frame(parent, width=parent.winfo_screenwidth() // 2, height=parent.winfo_screenheight() // 2)
        self.image_size = windll.user32.GetSystemMetrics(0) // 2, windll.user32.GetSystemMetrics(1) // 2

        self.bridge = bridge
        self.info_frame = info_frame
        self.admittance_frame = admittance_frame

        self.video_label: Optional[tk.Label] = None

    def generate_image(self, capture: VideoCapture) -> Image:
        frame_buffer, qr_codes = get_buffer_and_qr_codes(capture)

        if len(qr_codes) > 0:
            qr = qr_codes[0]
            self.admittance_frame.qr = qr

            if qr.data == utils.QR_DATA_PREVIOUS:
                frame_buffer = cv2.resize(frame_buffer, (self.image_size[0], self.image_size[1]))
                return PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_buffer, cv2.COLOR_BGR2RGBA)))

            utils.QR_DATA_PREVIOUS = qr.data

            request = self.bridge.verify(qr.data.decode('utf-8'))

            if request is not None:
                if request['text'] == 'valid':
                    self.admittance_frame.mark_attendance_button['state'] = 'active'
                else:
                    self.admittance_frame.mark_attendance_button['state'] = 'disabled'

            decoded = decode_qr(qr)
            if decoded is None:
                frame_buffer = cv2.resize(frame_buffer, (self.image_size[0], self.image_size[1]))
                return PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_buffer, cv2.COLOR_BGR2RGBA)))

            if decoded['type'] == '!STAFF!':
                pass_type = 'STAFF'
            elif decoded['type'] == '!ALL!':
                pass_type = 'ALL'
            else:
                pass_type = decoded['type']

            self.info_frame.set_data(decoded['_id'], decoded['name'], decoded['phone'], pass_type)

            draw_qr_bounding_box(frame_buffer, qr)

        frame_buffer = cv2.resize(frame_buffer, (self.image_size[0], self.image_size[1]))
        self.info_frame.update_pass_info_box(qr_codes)

        return PhotoImage(image=Image.fromarray(cv2.cvtColor(frame_buffer, cv2.COLOR_BGR2RGBA)))

    def refresh_image(self, photo_image: Optional[PhotoImage]):
        if photo_image is None:
            self.video_label = None

        if self.video_label is None:
            self.video_label = tk.Label(self.frame, image=photo_image)
        else:
            self.video_label.config(image=photo_image)

        self.video_label.image = photo_image
        self.video_label.pack(expand=True, fill=tk.BOTH)


def draw_qr_bounding_box(frame_buffer, qr):
    pt1x = min(qr.polygon[0].x, qr.polygon[1].x, qr.polygon[2].x, qr.polygon[3].x)
    pt1y = min(qr.polygon[0].y, qr.polygon[1].y, qr.polygon[2].y, qr.polygon[3].y)
    pt2x = max(qr.polygon[0].x, qr.polygon[1].x, qr.polygon[2].x, qr.polygon[3].x)
    pt2y = max(qr.polygon[0].y, qr.polygon[1].y, qr.polygon[2].y, qr.polygon[3].y)

    pt1 = (pt1x, pt1y)
    pt2 = (pt2x, pt2y)

    cv2.rectangle(frame_buffer, pt1, pt2, (0, 255, 0), 3)
