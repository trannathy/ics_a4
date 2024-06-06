'''

ds_protocol.py reads protocol-formated strings from and creates
protocol-adhering commands to send to the DSU server.

'''

# Replace the following placeholders with your information.

# THY TRAN
# THYNT1@UCI.EDU
# 90526048

import json
import time
import ds_client
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.

Response = namedtuple("Response", ["type", "message", "token"])


def extract_json(json_msg: str) -> tuple:
    '''

    Call the json.loads function on a json string and convert it to a
    DataTuple object

    '''

    ex_dict = json_to_dict(json_msg)
    try:
        ex_json = Response(ex_dict["type"], ex_dict["message"], ex_dict["token"])
    except KeyError:
         ex_json = Response(ex_dict["type"], ex_dict["messages"], ex_dict["token"])
    return ex_json


def json_to_dict(json_to_decode: str) -> dict:

    '''

    Decodes a json string to a dictionary

    '''

    try:
        json_obj = json.loads(json_to_decode)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None

    json_keys, json_values = get_dict_lists(json_obj)
    json_dict = dict(zip(json_keys, json_values))
    return json_dict


def get_dict_lists(svr_dict: dict) -> tuple:

    '''

    Gets the values of a a json dictionary as lists.

    '''

    keys = []
    values = []

    inner_dict = svr_dict["response"]

    for key in inner_dict:
        keys.append(key)
        values.append(inner_dict[key])

    if len(keys) < 3:
        keys.append("token")
        values.append(None)

    return keys, values


def create_join_msg(username: str, password: str) -> str:

    '''

    Creates a join message adhering to DSU protocol.

    '''

    msg = (f'{{"join": {{"username": "{username}", ' +
           f'"password": "{password}", "token": ""}}}}')
    return msg


def create_post_msg(post_entry: str, user_token: str) -> str:

    '''

    Creates a post message adhering to DSU protocol.

    '''

    post_as_str = (f'{{"entry": "{post_entry}", ' +
                   f'"timestamp": "{time.time()}"}}')
    msg = f'{{"token": "{user_token}", "post": {post_as_str}}}'
    return msg


def create_bio_msg(user_bio: str, user_token: str) -> str:

    '''

    Creates a bio message adhering to DSU protocol.

    '''

    bio_pub = f'{{"entry": "{user_bio}", "timestamp": "{time.time()}"}}'
    msg = f'{{"token": "{user_token}", "bio": {bio_pub}}}'
    return msg


def create_send_dm_message(user_message: str, user_recipient: str,
                           user_token: str) -> str:
    
    '''

    Creates a send dm message adhering to DSU protocol.

    '''

    dm = (f'{{"entry": "{user_message}", "recipient": "{user_recipient}", ' +
                f'"timestamp": "{time.time()}"}}')
    msg = f'{{"token": "{user_token}", "directmessage": {dm}}}'
    return msg


def create_unread_dm_message(user_token: str) -> str:
     
    '''

    Creates an unread dms request message adhering to DSU protocol.

    '''
   
    msg = f'{{"token": "{user_token}", "directmessage": "new"}}'
    return msg


def create_all_dm_message(user_token: str) -> str:
     
    '''

    Creates an all dms request message adhering to DSU protocol.

    '''
   
    msg = f'{{"token": "{user_token}", "directmessage": "all"}}'
    return msg


def get_msg_list_from_json(json_msg) -> list:
    svr_msg = extract_json(json_msg)
    messages_list = svr_msg.message
    return messages_list


def print_messages(messages_to_print: list[dict]) -> None:
    if len(messages_to_print) == 0:
        print("\nNo messages to show.\n")
    for msg in messages_to_print:
        print()
        print(f"From User: {msg['from']}")
        print(msg['message'])
        print(f"Time: {msg['timestamp']}")
    print()


def interpret_svr_message_list(svr_msg: str, output: bool):
    try:
        msg_list = get_msg_list_from_json(svr_msg)
        if output:
            print_messages(msg_list)
        return msg_list
    except Exception:
        raise ds_client.DSUServerError("COULD NOT INTERPRET SERVER MESSAGE")