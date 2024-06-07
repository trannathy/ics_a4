'''

ds_messenger is responsible for all the direct messaging.

'''
import time

import ds_client
import ds_protocol
import Profile

PORT = 3021


class DirectMessage:
    '''

    This class controls the dms that the user sends

    '''

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:

    '''

    This class is responsible for all the direct messenging

    '''

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None

    def connect_dm(self, output=True) -> dict:

        '''

        Tries to connect to the DSU server by establishing a socket
        connection and, if the socket connection is successful, tries
        sending a join message to the server.

        '''

        try:
            connection = ds_client.connect_to_server(self.dsuserver,
                                                     PORT, output)
            if output:
                print("SUCESSFULLY CONNECTED TO THE SERVER!")

        except Exception as exc:
            raise ds_client.DSUServerError("Could Not Connect") from exc

        ds_client.send_join(connection, self.username, self.password)
        svr_type, user_token = ds_client.interpret_svr_msg(connection,
                                                           output)

        if (svr_type != "error" and svr_type is not None):
            connection_dict = {"conn": connection, "token": user_token}
            return connection_dict

        raise ds_client.DSUServerError("Could Not Login")

    def send(self, recipient: str, message: str) -> bool:

        '''

        Tries sending a dm via the dsu server. First tries to connect to the
        server, and exits if connection fails. Returns true or false
        based on whether or not the dm send was successful

        '''

        try:
            dm_conn = self.connect_dm()

            connection = dm_conn["conn"]
            user_token = dm_conn["token"]

            new_dm = DirectMessage()
            new_dm.recipient = recipient
            new_dm.message = message
            new_dm.timestamp = time.time()

            ds_client.send_dm(connection, new_dm.recipient, new_dm.message,
                              user_token)
            svr_type, user_token = ds_client.interpret_svr_msg(connection)

            ds_client.disconnect(connection)

            if svr_type == "error" or svr_type is None:
                return False

            return True

        except ds_client.DSUServerError:
            return False

    def get_messages_list(self, conn: ds_client.Connection, token: str,
                          new: bool, output=True):

        '''

        Sends a request for messages (new only or all depending on the
        new argument). Then, prints the list of messages.

        '''

        try:
            if new:
                ds_client.send_new_req(conn, token)
            else:
                ds_client.send_all_req(conn, token)

            svr_msg = ds_client.read_message(conn)
            msg_list = ds_protocol.interpret_svr_message_list(svr_msg, output)

            return msg_list

        except ds_client.DSUServerError:
            return None

        except TypeError:
            return None

    def retrieve_new(self, print_out=True) -> list:

        '''

        Tries to retrieve any new messages from the server.
        If the user cannot connect to the server, returns nothing.
        If the user can connect to the server, then gets a list
        of new messages and returns it.
        The print_out argument determines if conformation messages
        are printed in the terminal.

        '''

        try:
            dm_conn = self.connect_dm(print_out)

            connection = dm_conn["conn"]
            user_token = dm_conn["token"]

            messages = self.get_messages_list(connection, user_token,
                                              True, print_out)

            ds_client.disconnect(connection, print_out)

            return messages

        except ds_client.DSUServerError:
            return None

    def retrieve_all(self, print_out=True) -> list:

        '''

        Tries to retrieve ALL messages from the server.
        If the user cannot connect to the server, returns nothing.
        If the user can connect to the server, then gets a list
        of new messages and returns it.
        The print_out argument determines if conformation messages
        are printed in the terminal.

        '''

        try:
            dm_conn = self.connect_dm(False)

            connection = dm_conn["conn"]
            user_token = dm_conn["token"]

            messages = self.get_messages_list(connection, user_token,
                                              False, print_out)

            ds_client.disconnect(connection)

            return messages

        except ds_client.DSUServerError:
            return None

    def save_dms_local(self, prof_path: str, new=False,
                       msg_hist=None) -> bool:

        '''

        Saves DMS into a local dsu profile and updates it. If a message
        list is provided, then only addes those. Otherwise, tries to retrieve
        from the server.

        '''

        if msg_hist is None and new:
            msg_hist = self.retrieve_all(False)
        elif msg_hist is None and not new:
            msg_hist = self.retrieve_new(False)

        profile = Profile.Profile()
        profile.load_profile(prof_path)

        if (msg_hist is not None and profile.username == self.username
                and profile.password == self.password
                and profile.dsuserver == self.dsuserver):

            profile.update_messages(msg_hist)
            profile.save_profile(prof_path)
            return True

        print("Could not locally save dms")
        return False
