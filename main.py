# import ctypes
# import subprocess
# import tkinter as tk
#
# import PIL.Image
# import PIL.ImageTk
# import cv2
# import queue
# import threading
# import time
# from pyzbar.pyzbar import decode
#
# from utils.video_capture import VideoCapture
#
# user32 = ctypes.windll.user32
# screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#
# # ADB forward the server running at port 5000 on remote to 5000 on localhost
# # subprocess.run(["adb", "forward", "tcp:5000", "tcp:5000"])
#
#
# # Wrapper for the cv2.VideoCapture class
# # Its only purpose is to make sure you always get the latest frame
# # Runs in a separate thread
# # Also makes it a pain to properly stop the scanner process since Ctrl+C only kills the main thread but this
# # Keeps running :P
# # ^Something to fix l8r.
# # Hitting "stop" twice terminates it just fine, though - just do that for now
#
#
# # Get the video feed from the default URL that IPWebcam uses
# vfeed = VideoCapture("http://localhost:5000/video")
#
#
# # QR reader
# # Runs at a max of 5 FPS
# # Callback is the function invoked when the QR is detected
# # root and canvas are tkinter elements
# def readUntilQR(callback, canvas, root):
#     while True:
#         # Capture frame-by-frame
#         frame = vfeed.read()
#         if frame is not None:
#             # Used to set max framerate
#             time.sleep(0.2)
#
#             # Grab the QR is any
#             # This returns an array with all QR codes in the frame
#             x = decode(frame)
#
#             # Check if there were any QRs
#             if len(x) != 0:
#                 # Draw a box around any detected QRs
#                 for qr in x:
#                     pt1x = min(qr.polygon[0].x, qr.polygon[1].x, qr.polygon[2].x, qr.polygon[3].x)
#                     pt1y = min(qr.polygon[0].y, qr.polygon[1].y, qr.polygon[2].y, qr.polygon[3].y)
#                     pt2x = max(qr.polygon[0].x, qr.polygon[1].x, qr.polygon[2].x, qr.polygon[3].x)
#                     pt2y = max(qr.polygon[0].y, qr.polygon[1].y, qr.polygon[2].y, qr.polygon[3].y)
#                     pt1 = (pt1x, pt1y)
#                     pt2 = (pt2x, pt2y)
#
#                     cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 3)
#
#             # Resize the frame to fit in the canvas (1/4th of the screensize)
#             frame = cv2.resize(frame, (vfeed.Ewidth, vfeed.Eheight))
#
#             # Conversions to make the image load in the canvas element
#             conv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#             cap_frame = PIL.Image.fromarray(conv_frame)
#             image = PIL.ImageTk.PhotoImage(image=cap_frame)
#
#             # Display the image onto the tkinter canvas
#             canvas.create_image(vfeed.Ewidth // 2, vfeed.Eheight // 2, image=image)
#             root.update()
#
#             # Invoke the callback function
#             # This is done after the rectangle drawing and display so that the operator sees the camera output
#             # And the rectangles drawn around QRs
#             # Before the execution is halted by the blocking callback function
#
#             if len(x) != 0:
#                 callback(x)
#
#             # Press q to close the video windows before it ends if you want
#             # This is for debugging only - remove this in the final release
#             # In the final release, just add a close button somewhere in the app
#             if cv2.waitKey(22) & 0xFF == ord('q'):
#                 break
#             # Pressing Q does NOT stop the second thread (VideoCapture wrapper)
#             # Therefore, to close the app fully, you need to actually press Q and then still Ctrl+C the execution
#             # If you're using PyCharm, then press the red "stop" button TWICE to properly kill the app
#
#         else:
#             # Actually, there is no way to reinitialize the video feed once it breaks
#             # Instead of retrying, just exit gracefully and ask the user to restart
#             # This code is stupid
#             print("No Video Feed! Retrying...")
#             time.sleep(1)
#
#
# # Invoked whenever a QR is found and the QR object is passed to it
# # QR object is an array of all the QR codes detected, each element in the array is a QR code object
# # See pyzbar documentation for a better explanation
# # Note: This is synchronous, so it will stop the processing of subsequent frames while it runs
# # This is intentional (I need playback to pause while the webserver calls are made)
# def processQR(decodedData):
#     print('Decoder')
#
#
# # Starts main process - Invoked by tkinter after a 5ms delay when the window opens
# def start():
#     readUntilQR(processQR, canvas, root)
#
#
# # Basic tkinter init, feel free to improve this
# root = tk.Tk()
# root.attributes('-fullscreen', True)
# root.title('Ticket Validation Kiosk')
# canvas = tk.Canvas(root, width=vfeed.Ewidth, height=vfeed.Eheight)
# canvas.pack(anchor='nw')
#
# # Start the app
# root.after(5, start)
# root.mainloop()
