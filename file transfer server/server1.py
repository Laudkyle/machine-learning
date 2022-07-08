import socket
import os
from tkinter import filedialog

s = socket.socket()
host = socket.gethostname()
hostip = socket.gethostbyname(host)
port = 12365
s.bind((hostip, port))

s.listen(10)
print('Hostname : ', host)
print(hostip)
c, addr = s.accept()
print(addr, "Connection Successful")

files = filedialog.askopenfilenames()
filedir = os.path.dirname(files[0])
num_files = len(files)
os.chdir(filedir)
c.send(bytes(str(num_files), 'utf-8'))
for i in range(num_files):
    file = files[i]
    filename = os.path.basename(file)
    c.send(bytes(filename, 'utf-8'))
    file = open(filename, 'rb')
    filedata = file.read(1024)
    print(f"Sending {filename}, Please wait...")
    while filedata:
        c.send(filedata)
        filedata = file.read(1024)
    file.close()

    print('DONE')
