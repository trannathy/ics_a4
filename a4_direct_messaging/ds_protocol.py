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
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.

Response = namedtuple("Response", ["type", "message", "token"])


def extract_json(json_msg: str) -> tuple:
    '''

    Call the json.loads function on a json string and convert it to a
    DataTuple object

    '''

    ex_dict = json_to_dict(json_msg)
    ex_json = Response(ex_dict["type"], ex_dict["message"], ex_dict["token"])
    return ex_json


def json_to_dict(json_to_decode: str):

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


def get_dict_lists(svr_dict: dict):

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


def create_join_msg(username, password):

    '''

    Creates a join message adhering to DSU protocol.

    '''

    msg = (f'{{"join": {{"username": "{username}", ' +
           f'"password": "{password}", "token": ""}}}}')
    return msg


def create_post_msg(post_entry, user_token):

    '''

    Creates a post message adhering to DSU protocol.

    '''

    post_as_str = (f'{{"entry": "{post_entry}", ' +
                   f'"timestamp": "{time.time()}"}}')
    msg = f'{{"token": "{user_token}", "post": {post_as_str}}}'
    return msg


def create_bio_msg(user_bio, user_token):

    '''

    Creates a bio message adhering to DSU protocol.

    '''

    bio_pub = f'{{"entry": "{user_bio}", "timestamp": "{time.time()}"}}'
    msg = f'{{"token": "{user_token}", "bio": {bio_pub}}}'
    return msg
