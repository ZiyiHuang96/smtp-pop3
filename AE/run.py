from socket import *
import socket
server_port = 30001
server_name = socket.gethostname()
AE_server = socket.socket(AF_INET,SOCK_STREAM)
AE_server.bind((server_name,server_port))
AE_server.listen(2)
print ('The server is ready to receive')
sockets = []
response = 'False'
toIP = ''
toPort = -1
while True:
    AESocket, addr = AE_server.accept()
    sockets.append(AESocket)
    message = AESocket.recv(2048).decode()
    print('message:', message)
    if message == 'HELO':
        AESocket.send('250'.encode())
    if message == 'MAIL FROM':
        AESocket.send('250 Sender ok'.encode())
    if message.split(':')[0] == 'RCPT TO':
        address = message.split(':')[1]
        toIP = address.split('@')[0]
        toPORT = address.split('@')[1]
        ms = 'connect:'+server_name+'@'+str(server_port)
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((toIP,int(toPORT)))
        clientSocket.send(ms.encode())
    if message == 'working':
        sockets[-2].send('250 Recipient ok'.encode())
    if message == 'DATA':
        AESocket.send('354'.encode())
    if message.split(':')[0] == 'email':
        clientSocket = socket.socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((toIP,int(toPORT)))
        clientSocket.send(message.encode())
    if message == '.':
        AESocket.send('250 Message accepted for delivery'.encode())
    if message == 'file saved':
        response = '200'
        sockets[-2].send(response.encode())