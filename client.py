import socket
# TCP
tcpSock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
tcpSock.connect((socket.gethostname(), 8080))

# UDP
udpSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Establish TCP connection
msg = tcpSock.recv(1024).decode()
print(msg)

bufferSize = 1024*1024*100

# Receive input from keyboard
while True:
    data = input(str())
    tcpSock.send(bytes(data, "utf-8"))

    if data == "exit":
        print("Exiting")
        tcpSock.close()
        udpSock.close()
        exit(1)

    elif data == "listallfiles":
        files = tcpSock.recv(1024).decode()
        print(files)

    elif data == "download all":
        file_num = tcpSock.recv(1024).decode()
        fn = int(file_num)
        files = tcpSock.recv(1024).decode()
        # TCP
        for i in range(fn):
            f_name = files.split()[i]
            file_received = open(f_name, 'wb')
            file_data = tcpSock.recv(bufferSize)
            file_received.write(file_data)
            file_received.close()

        print(f"Downloaded {files}")
    else:
        # download <filename>
        if data.split()[0] != "download":
            print("Incorrect input, please try again!")
            continue

        fileName = data.split()[-1]
        # create UDP port
        message = "Hello UDP Server!"
        udpSock.sendto(message.encode("utf-8"), (socket.gethostname(), 8888))

        file_received = open(fileName, 'wb')
        file_data = udpSock.recv(bufferSize)

        file_received.write(file_data)
        file_received.close()
        print("Downloaded " + fileName)




