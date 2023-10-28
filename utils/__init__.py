import base64
import binascii
import json
from typing import Optional

import cv2
from pyzbar import pyzbar

from utils.video_capture import VideoCapture

INVERT_COLOR = False
QR_DATA_PREVIOUS = b''


def get_buffer_and_qr_codes(capture: VideoCapture):
    frame_buffer = capture.read()

    if frame_buffer is None:
        return None

    if INVERT_COLOR:
        frame_buffer = cv2.bitwise_not(frame_buffer)

    return frame_buffer, pyzbar.decode(frame_buffer)


def decode_qr(qr) -> Optional[dict]:
    qr_data = qr.data.decode('utf-8').split('.')

    if len(qr_data) != 3:
        return None

    try:
        qr_string = base64.b64decode((qr_data[1] + '=' * 5).encode())
        qr_json = json.loads(qr_string)

        return qr_json

    except binascii.Error as e:
        print(f'Base64 Decoding Error: {e}')
        return None

    except json.JSONDecodeError as e:
        print(f'JSON Decoding Error: {e}')
        return None
