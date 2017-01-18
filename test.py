'''
Varun Ved
Brandon Sherman

CSC138
mail.py

simple mail client
'''

'''
imports
'''
from socket import *
import base64
import ssl


'''
constants
'''
#google mail server requirements
MAILSERVER = 'smtp.gmail.com'
MAILPORT = 465
BYTE_SIZE = 1024

#statuses
RECV_220 = '220'
RECV_250 = '250'

#all messages must end in \r\n
END_MSG = '\r\n'

#email/passwd for my account
EMAIL = 'databoyz69@gmail.com'
PASSWORD = 'booboobear'

#message constants
HELO_MSG = 'HELO databoyz'
AUTH_LOGIN = 'AUTH LOGIN'
FROM_MSG = 'MAIL FROM: <' + EMAIL + '>'
RCPT_MSG = 'RCPT TO: <' + EMAIL + '>'

'''
methods
'''
#handle 220, 250 statuses
def statusCodeHandler(recv, expected):
    if recv[:3] != expected:
        print(expected + ' not recieved')
    else:
        print(expected + ' recieved')

#create instance of a mail socket
def createMail():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket = ssl.wrap_socket(clientSocket)
    clientSocket.connect((MAILSERVER, MAILPORT))
    recv = clientSocket.recv(BYTE_SIZE)
    statusCodeHandler(recv, RECV_220)
    return clientSocket

#send message with passed socket, check if encryption
#or status handling required
def send(msg, sock, b64, status):
    if b64 == True:
        sock.send(base64.b64encode(msg) + END_MSG)
    if b64 != True:
        sock.send(msg + END_MSG)
    recv = sock.recv(1024)
    if status == True:
        statusCodeHandler(recv, RECV_250)
    print(recv)

#read message from command line
def getInput():
    msg = raw_input('What would you like to say? ')
    return(msg + END_MSG + '.')

#send required messages
def run():
    sock = createMail()
    send(HELO_MSG, sock, False, True)
    send(AUTH_LOGIN, sock, False, False)
    send(EMAIL, sock, True, False)
    send(PASSWORD, sock, True, False)
    send(FROM_MSG, sock, False, True)
    send(RCPT_MSG, sock, False, True)
    send('DATA', sock, False, False)
    send(getInput(), sock, False, False)
    send('QUIT', sock, False, False)
    sock.close()

run()
