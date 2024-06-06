'''

ds_client.py is responsible for connecting a3 to and communicating wth the
ICS 32 DSU Server.

'''

# THYNT1
# THYNT1@UCI.EDU
# 90526048

import ds_protocol
from collections import namedtuple
import socket



OUTPUT_DSU_SERVER_ERROR = "ERROR: COULD NOT CONNECT TO OR READ FROM THE SERVER"
Connection = namedtuple('Connection', ['socket', 'send', 'recv'])


class DSUServerError(Exception):

    '''

    Custom exception for when there is trouble connecting to the DSU server.

    '''


def send(server: str, port: int, username: str, password: str, message: str,
         bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''

    try:
        connection = connect_to_server(server, port)

        print("SUCESSFULLY CONNECTED TO THE SERVER!")
        send_join(connection, username, password)
        svr_type, user_token = interpret_svr_msg(connection)

        if (svr_type != "error" and svr_type is not None) and message != "":
            send_post(connection, message, user_token)
            svr_type, user_token = interpret_svr_msg(connection)

        if (svr_type != "error" and svr_type is not None) and bio is not None:
            send_bio(connection, bio, user_token)
            svr_type, user_token = interpret_svr_msg(connection)

        disconnect(connection)

        if svr_type == "error" or svr_type is None:
            return False

        return True

    except DSUServerError:
        return False


def send_join(conn: Connection, user: str, pwd: str):

    '''

    Sends a json message to the DSU server to log in

    '''

    join_msg = ds_protocol.create_join_msg(user, pwd)
    write_to_svr(conn, join_msg)


def send_post(conn: Connection, entry: str, token: str):

    '''

    Sends a json message to the DSU server to publish a post

    '''

    post_msg = ds_protocol.create_post_msg(entry, token)
    write_to_svr(conn, post_msg)


def send_bio(conn: Connection, new_bio: str, token: str):

    '''

    Sends a json message to the DSU server to publish a user bio.

    '''

    bio_msg = ds_protocol.create_bio_msg(new_bio, token)
    write_to_svr(conn, bio_msg)


def send_dm(conn: Connection, rec: str, msg: str, 
                token: str):
  
        '''

        Sends a json message to the DSU server to send a dm

        '''

        send_dm_msg = ds_protocol.create_send_dm_message(msg, rec, token)
        write_to_svr(conn, send_dm_msg)


def send_new_req(conn: Connection, token: str):
          
        '''

        Sends a json message to the DSU server to request unread/new messages

        '''

        send_new_req_msg = ds_protocol.create_unread_dm_message(token)
        write_to_svr(conn, send_new_req_msg)

def send_all_req(conn: Connection, token: str):
          
    '''

    Sends a json message to the DSU server to request all messages

    '''

    send_new_all_msg = ds_protocol.create_all_dm_message(token)
    write_to_svr(conn, send_new_all_msg)


def connect_to_server(host: str, port: int, output = True) -> None:

    '''

    Creates a socket to connect to the DSU Server

    '''

    try:
        if output:
            print(f"Connecting to host {host} at port {port}")
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((host, port))

        connection = make_connection(my_socket)
        return connection

    except ConnectionRefusedError as cre:
        raise DSUServerError(OUTPUT_DSU_SERVER_ERROR) from cre

    except ConnectionAbortedError as cae:
        raise DSUServerError(OUTPUT_DSU_SERVER_ERROR) from cae

    except ConnectionError as ce:
        raise DSUServerError(OUTPUT_DSU_SERVER_ERROR) from ce


def disconnect(conn: Connection, output=True):

    '''

    Closes the socket and its associated files to disconnect from the
    DSU server.

    '''

    conn.send.close()
    conn.recv.close()
    conn.socket.close()
    if output:
        print("DISCONNECTED")


def write_to_svr(conn: Connection, message_to_send: str):

    '''

    Sends a message to the DSU server.

    '''

    try:
        conn.send.write(message_to_send + "\n")
        conn.send.flush()

    except Exception as exc:
        raise DSUServerError("COULD NOT SEND MESSAGE TO THE SERVER") from exc


def make_connection(sock: socket) -> Connection:

    '''

    Creates files to store communication through a socket.

    '''

    f_send = sock.makefile('w')
    f_recv = sock.makefile('r')

    return Connection(socket=sock, send=f_send, recv=f_recv)


def read_message(conn: Connection) -> str:

    '''

    Reads back a message received from the DSU server.

    '''

    try:
        received = conn.recv.readline()[:-1]
        return received

    except EOFError:
        return None


def interpret_svr_msg(conn: Connection, output=True) -> tuple:

    '''

    Decodes the message sent from the server and prints it back to the user.

    '''

    try:
        svr_msg = ds_protocol.extract_json(read_message(conn))
        if output:
            print_svr_msg(svr_msg.type, svr_msg.message)
        return svr_msg.type, svr_msg.token

    except DSUServerError:
        if output:
            print("ERROR: COULD NOT READ SERVER MESSGAE")
        return None, None

    except TypeError:
        if output:
            print("ERROR: COULD NOT READ SERVER MESSGAE")
        return None, None


def print_svr_msg(msg_type, msg) -> str:

    '''

    Prints the message that the server sent in a readable format.

    '''

    if msg_type == "error":
        print("ERROR: ", end="")

    if msg is not None:
        print(msg)
