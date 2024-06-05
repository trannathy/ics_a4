'''

ds_messenger is responsible for all the direct messaging

'''

import ds_client
import ds_protocol
import Profile
import ui
import shlex

PORT = 3021

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.timestamp = None


class DirectMessenger:

    def __init__(self, dsuserver: str, username: str, password: str):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
            
    def send(self, recipient:str, message:str) -> bool:
        # must return true if message successfully sent, false if send failed.
        try:
            dm_conn = self.connect_dm()

            if dm_conn is None:
                raise ds_client.DSUServerError

            else:
                connection = dm_conn["conn"]
                user_token = dm_conn["token"]

                ds_client.send_dm(connection, recipient, message, user_token)
                svr_type, user_token = ds_client.interpret_svr_msg(connection)

                ds_client.disconnect(connection)

                if svr_type == "error" or svr_type is None:
                    return False

            return True

        except ds_client.DSUServerError:
            return False
            
    def retrieve_new(self):
        # must return a list of DirectMessage objects containing all new messages
        try:
            dm_conn = self.connect_dm()

            if dm_conn is None:
                raise ds_client.DSUServerError("ERROR")

            else:
                connection = dm_conn["conn"]
                user_token = dm_conn["token"]


                messages = self.get_messages_list(connection, user_token, new = True)

                ds_client.disconnect(connection)

                print(messages) #test
                return messages
    
        except ds_client.DSUServerError:
            print("ERROR: MESSAGES NOT RETRIEVED")
            return None

    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages
        try:
            dm_conn = self.connect_dm()

            if dm_conn is None:
                raise ds_client.DSUServerError("ERROR")

            else:
                connection = dm_conn["conn"]
                user_token = dm_conn["token"]

                messages = self.get_messages_list(connection, user_token, new = False)
                
                ds_client.disconnect(connection)

                print(messages) #test
                return messages
    
        except ds_client.DSUServerError:
            print("ERROR: MESSAGES NOT RETRIEVED")
            return None

    def connect_dm(self):
        
        connection = ds_client.connect_to_server(self.dsuserver, PORT)

        print("SUCESSFULLY CONNECTED TO THE SERVER!")
        ds_client.send_join(connection, self.username, self.password)
        svr_type, user_token = ds_client.interpret_svr_msg(connection)

        if (svr_type != "error" and svr_type is not None):
            return {"conn": connection, "token": user_token}

        if svr_type == "error" or svr_type is None:
            print("ERROR: CONNECT_DM")
            return None

    def get_messages_list(self, conn: ds_client.Connection, token: str,
                          new: bool) -> list:
        try:
            if new:
                ds_client.send_new_req(conn, token)
            else:
                ds_client.send_all_req(conn, token)
            svr_msg = (ds_client.read_message(conn))
            msg_list = ds_protocol.interpret_svr_message_list(svr_msg)
            return msg_list

        except ds_client.DSUServerError:
            print("ERROR: COULD NOT READ SERVER MESSGAE")
            return None

        except TypeError:
            print("ERROR: COULD NOT READ SERVER MESSGAE")
            return None

    def dm_command_intake(self, path: str, mode: bool) -> str:
    
        '''

        Gets a dm command from the user

        '''

        profile = Profile.Profile()
        profile.load_profile(path)

        user_input = input(ui.direct_messaging_ui(profile.username, mode))
        return user_input

    def dm_command_check_validity(self, command_line: str) -> bool:

        '''

        Makes sure that the dm command is an option

        '''

        if command_line[0] == "DM" and len(command_line) == 3:
            return True

        elif command_line[0] in ["UNREAD", "ALL"] and len(command_line) == 1:
            return True

        print(ui.OUTPUT_COMMAND_INVALID)
        return False

    def dm_run(self, path: str, mode: bool):
    
        '''

        Asks for dm commands and runs them

        '''

        dm_command = self.dm_command_intake(path, mode)

        if dm_command.strip() != "Q":
            try:
                dm_command = shlex.split(dm_command)

            except ValueError:
                print(ui.OUTPUT_COMMAND_INVALID)
                self.dm_run(path, mode)
        
            else:
                if self.dm_command_check_validity(dm_command) is False:
                    pass

                elif dm_command[0] == "DM":

                    self.send(dm_command[1], dm_command[2])

                elif dm_command[0] == "UNREAD":
                    self.retrieve_new()

                elif dm_command[0] == "ALL":
                    self.retrieve_all()

                self.dm_run(path, mode)
