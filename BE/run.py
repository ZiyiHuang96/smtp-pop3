from socket import *
import socket
def utf8len(s):
    return len(s.encode('utf-8'))

server_port = 30002
server_name = socket.gethostname()
BE_server = socket.socket(AF_INET,SOCK_STREAM)
BE_server.bind((server_name,server_port))
BE_server.listen(2)
fromIP = ''
fromPort = -1
print ('The server is ready to receive')
while True:
    BESocket, addr = BE_server.accept()
    message = BESocket.recv(2048).decode()
    print('message:', message)
    if message.split(':')[0] == 'connect':
        body = message.split(':')[1]
        fromIP = body.split('@')[0]
        fromPort = body.split('@')[1]
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((fromIP,int(fromPort)))
        clientSocket.send('working'.encode())
    if message.split(':')[0] == 'email':
        f = open("email.txt", "a")
        f.write(message.split(':')[1])
        f.write("\n")
        f.close()
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((fromIP,int(fromPort)))
        clientSocket.send('file saved'.encode())

    if message == 'user':
        BESocket.send('+OK'.encode())

    if message == 'list':
        lines = []
        i = 0
        try:
            with open("email.txt") as file_in:
                for line in file_in:
                    info = str(i) + ' ' + str(utf8len(line))
                    lines.append(info)
        except IOError:
            lines = []
        lines = str(lines)
        BESocket.send(lines.encode())

    if message == 'retr':
        lines = []
        i = 0
        try:
            with open("email.txt") as file_in:
                for line in file_in:
                    lines.append(line.rstrip())
        except IOError:
            lines = []
        lines = str(lines)
        BESocket.send(lines.encode())

    # connectionSocket.close()