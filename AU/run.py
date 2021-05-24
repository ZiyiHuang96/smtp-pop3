from flask import Flask
from datetime import date
from flask import Flask, request, jsonify, abort
from socket import *
import socket
client_name = socket.gethostname()
client_port = 30000
app = Flask(__name__)

@app.route('/email')
def send():
    fromArg = request.args.get('from')
    toArg = request.args.get('to')
    messageArg = request.args.get('message')
    if not fromArg or not toArg or not messageArg:
        abort(400)
    
    try: 
        fromIP = str(fromArg).split(':')[0]
        fromPORT = str(fromArg).split(':')[1]
        toIP = str(toArg).split(':')[0]
        toPORT = str(toArg).split(':')[1]
        fromPORT = int(fromPORT)
        toPORT = int(toPORT)
        message_content = str(messageArg)
    except ValueError:
        abort(400)
    serverName = fromIP
    serverPort = int(fromPORT)

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('HELO'.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '250':
        return jsonify('response of HELO is not 250'), 400
    clientSocket.close()
    
    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('MAIL FROM'.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '250 Sender ok':
        return jsonify('response of MAIL FROM is not 250 Sender ok'), 400
    clientSocket.close()

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    ms = 'RCPT TO:' + toIP + '@' + str(toPORT)
    clientSocket.send(ms.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '250 Recipient ok':
        return jsonify('response of RCPT TO is not 250 Recipient ok'), 400
    clientSocket.close()

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('DATA'.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '354':
        return jsonify('response of DATA is not 354'), 400
    clientSocket.close()

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    ms = 'email:' + message_content
    clientSocket.send(ms.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '200':
        return jsonify('file saved error'), 400
    clientSocket.close()

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('.'.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '250 Message accepted for delivery':
        return jsonify('delivery error'), 400
    clientSocket.close()
    
    return jsonify({'from' : fromArg, 'to' : toArg, 'message' : messageArg, 'response' : response.decode()}), 200

app.run(host='0.0.0.0',
        port=30000,
        debug=True)
