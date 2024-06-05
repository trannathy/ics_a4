import ds_protocol
import socket
from collections import namedtuple

HOST = "168.235.86.101"
PORT = 3021

Connection = namedtuple('Connection', ['socket', 'send', 'recv'])

def create_connection():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((HOST, PORT))
    f_send = my_socket.makefile('w')
    f_recv = my_socket.makefile('r')
    return Connection(socket=my_socket, send=f_send, recv=f_recv)

def test_send_dm():
    username = "thynt1"
    password = "206060"
    recipient = "nathalien"
    token = "d4bb7e73-1538-410e-8edb-2f9a1a89be35"