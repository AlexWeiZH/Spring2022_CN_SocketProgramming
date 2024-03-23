import socket
import os
# TCP
tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSock.bind((socket.gethostname(), 8080))
tcpSock.listen(5)

# UDP
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSock.bind((socket.gethostname(), 8888))

bufferSize = 1024*1024*100

print("Server running...")

clientSocket, address = tcpSock.accept()
msg = "Server connected!!!"
clientSocket.send(bytes(msg, "utf-8"))

def getFileName(path):
    for root, dirs, files1 in os.walk(path):
       print(files1)
    return files1


while True:
    data = clientSocket.recv(1024).decode()

    if data == "exit":
        clientSocket.close()

    elif data == "listallfiles":
        files = getFileName("./")
        length = len(files)
        file_string = ""
        for i in range(length):
            file_string += files[i]
            if i != length-1:
                file_string += " "

        clientSocket.send(bytes(file_string.encode('utf-8')))

    elif data == "download all":
        files = getFileName("./")
        file_nubmers = len(files)
        clientSocket.send(bytes(str(file_nubmers), "utf-8"))

        file_string = ""
        for i in range(file_nubmers):
            file_string += files[i]
            if i != file_nubmers - 1:
                file_string += " "

        clientSocket.send(bytes(file_string.encode('utf-8')))

        for i in range(file_nubmers):
            fileName = files[i]
            target_file = open(fileName, 'rb')
            target_data = target_file.read(bufferSize)
            # TCP
            clientSocket.send(target_data)

    else:
        # download <filename>
        if data.split()[0] != "download":
            print("Incorrect input, please try again!")
            continue

        fileName = data.split()[-1]
        message, addr = udpSock.recvfrom(1024)

        target_file = open(fileName, 'rb')
        target_data = target_file.read(bufferSize)
        # UDP
        udpSock.sendto(target_data, addr)

