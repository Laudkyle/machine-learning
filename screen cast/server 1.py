import socket, cv2,pickle,struct,ctypes, win32gui, win32ui
import datetime
from threading import Thread
import pyautogui
from PIL import Image, ImageGrab, ImageDraw
import numpy as np
from win32api import GetSystemMetrics


# Creating socket


width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)

print('Host IP :', host_ip)

port = 9999
socket_address = (host_ip,port)

#socket bind
server_socket.bind(socket_address)

#socket Listen
server_socket.listen(5)
print("Listening")


def get_cursor():
    hcursor = win32gui.GetCursorInfo()[1]
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, 36, 36)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), hcursor)

    bmpinfo = hbmp.GetInfo()
    bmpbytes = hbmp.GetBitmapBits()
    bmpstr = hbmp.GetBitmapBits(True)
    cursor = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert(
        "RGBA")

    win32gui.DestroyIcon(hcursor)
    win32gui.DeleteObject(hbmp.GetHandle())
    hdc.DeleteDC()

    return cursor


def pointer_ellipse(image_path, output_path, xpos, ypos):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image,'RGBA')
    draw.ellipse((100, 150, 275, 300), outline="black", width=1, fill=(100, 100, 0, 128))
    draw.ellipse((xpos-30, ypos-30, xpos+30, ypos+30), outline="black", width=1, fill=(100, 100, 0, 128))
    image.save(output_path)

def send_commands():
    position = pyautogui.position()
    poss = f"{position[0]},{position[1]}"
    client_socket.send(bytes(poss, 'utf8'))

# thread2 = Thread(target=send_commands)
size = round(ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100 * 32)


#socket accept
while True:
    client_socket,addr = server_socket.accept()
    print('Connection successful')
    if client_socket:
        while True:
            img = ImageGrab.grab(bbox=(0, 0, width, height))
            cursor = get_cursor()

            pixdata = cursor.load()
            minsize = [size, None]

            width1, height1 = cursor.size
            for y in range(height1):
                for x in range(width1):

                    if pixdata[x, y] == (0, 0, 0, 255):
                        pixdata[x, y] = (0, 0, 0, 0)

                    else:
                        if minsize[1] == None:
                            minsize[1] = y

                        if x < minsize[0]:
                            minsize[0] = x
            ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
            pos_win = win32gui.GetCursorPos()
            pos = (round(pos_win[0] * ratio), round(pos_win[1] * ratio))
            img.paste(cursor, pos, cursor)
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            a = pickle.dumps(frame)
            position = pyautogui.position()
            poss = f"{position[0]},{position[1]}"
            poss = pickle.dumps(poss)
            message = struct.pack("Q",len(a))+a
            client_socket.sendall(message)
            # cv2.imshow("TRANSMITTING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()

