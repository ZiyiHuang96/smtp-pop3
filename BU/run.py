from flask import Flask
from datetime import date
from flask import Flask, request, jsonify, abort
from socket import *
import socket
client_name = socket.gethostname()
client_port = 30003
app = Flask(__name__)

@app.route('/email')
def send():
    fromArg = request.args.get('from')
    if not fromArg:
        abort(400)
    
    try: 
        fromIP = str(fromArg).split(':')[0]
        fromPORT = str(fromArg).split(':')[1]
    except ValueError:
        abort(400)
    serverName = fromIP
    serverPort = int(fromPORT)

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('user'.encode())
    response = clientSocket.recv(2048)
    if response.decode() != '+OK':
        return jsonify('response of user is not +OK'), 400
    clientSocket.close()
    
    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('list'.encode())
    response_list = clientSocket.recv(2048)
    clientSocket.close()

    clientSocket = socket.socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send('retr'.encode())
    response = clientSocket.recv(2048)
    clientSocket.close()

    return jsonify({'from' : fromArg, 'emails by retr' : str(response.decode()), 'emails by list' : str(response_list.decode())}), 200

app.run(host='0.0.0.0',
        port=30003,
        debug=True)
