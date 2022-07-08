import socket
import os

c = socket.socket()
host = input(str('Please Enter Your Host Name \n'))
c.connect((host, 12365))
print("Connection Successful")
files = []
num = c.recv(1024).decode('utf-8')
print(num)
num = int(num)
num_recv = num
while num != 0:
    filename = c.recv(1024)
    files.append(filename)
    num -= 1
print(files)
for i in range(num_recv):
    file = files[i]
    with open(file, 'wb')as f:
        filedata = c.recv(1024)
        print(f"Receiving {file}....Please Wait...")
        while filedata:
            f.write(filedata)
            filedata = c.recv(1024)
print("Transfer Complete...")
print(f'Files received are {files}')