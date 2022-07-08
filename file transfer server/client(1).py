import socket
import os

c = socket.socket()
#host = input(str('Please Enter Your Host Name \n'))
c.connect(('127.0.0.1', 12365))
print("Connection Successful")
files = []
num = c.recv(1024).decode('utf-8')
print(num)
num = int(num)
while num != 0:
    filename = c.recv(1024).decode('utf-8')
    files.append(filename)
    for file in filenames:
        f = open(file, 'wb')
        print(file)
        while True:
            filedata = c.recv(1024)
            print("RECIEVING FILE....PLESE WAIT...")
            while filedata:
                f.write(filedata)
                filedata = c.recv(1024)
            f.close()
            break
        print("Transfer Complete...")
    num -= 1
print(f'Files recieved are {files}')