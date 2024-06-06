'''
Profile.py

ICS 32
Assignment #2: Journal

Author: Mark S. Baldwin, modified by Alberto Krone-Martins

v0.1.9

You should review this code to identify what features you need to support
in your program for assignment 2.

YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS
CODE RIGHT NOW, though can you certainly take a look at it if you are curious
since we already covered a bit of the JSON format in class.
'''

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """

    DsuFileError is a custom exception handler that you should catch in your
    own code. It is raised when attempting to load or save Profile objects t
    file the system.

    """


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in
    your own code. It mis raised when attempting to deserialize a dsu file
    to a Profile object.

    """


class Post(dict):
    """

    The Post class is responsible for working with individual user posts. It
    currently supports two features: A timestamp property that is set upon
    instantiation and when the entry object is set and an entry property that
    stores the post message.

    The property method is used to support get and set capability for entry
    and time values. When the value for entry is changed, or set, the
    timestamp field is updated to the current time.

    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):

        '''

        Sets a post entry and also a timestamp based on the current time.

        '''

        self._entry = entry
        dict.__setitem__(self, 'entry', entry)
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):

        '''

        Gets the message/entry belonging to the post
        '''

        return self._entry

    def set_time(self, timestamp: float):

        '''

        Sets a timestamp for the post

        '''

        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):

        '''

        Gets the time from the post

        '''

        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Messages(dict):
    """

    The Messages class is responsible for working with the messages that
    a user has reeived in the past, allowing local storage so that the
    messages are accessible without an internet connection.

    """

    def __init__(self, msg: str, sender: str, timestamp: float):
        self.msg = msg
        self.sender = sender
        self.timestamp = timestamp

        dict.__init__(self, msg=self.msg, sender=self.sender,
                      timestamp=self.timestamp)


class Profile:
    """

    The Profile class exposes the properties required to join an ICS 32 DSU
    server. You will need to use this class to manage the information provided
    by each new user created within your program for a2. Pay close attention to
    the properties and functions in this class as you will need to make use of
    each of them in your program.

    When creating your program you will need to collect user input for the
    properties exposed by this class. A Profile class should ensure that a
    username and password are set, but contains no conventions to do so. You
    should make sure that your code verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''             # OPTIONAL
        self._posts = []          # OPTIONAL
        self._messages = {}        # OPTIONAL

    def add_post(self, post: Post) -> None:

        """

        add_post accepts a Post object as parameter and appends it to the posts
        list. Posts are stored in a list object in the order they are added. So
        if multiple Posts objects are created, but added to the Profile in a
        different order, it is possible for the list to not be sorted by the
        Post.timestamp property. So take caution as to how you implement your
        add_post code.

        """

        self._posts.append(post)

    def del_post(self, index: int) -> bool:

        """

        del_post removes a Post at a given index and returns True if successful
        and False if an invalid index was supplied.

        To determine which post to delete you must implement your own search
        operation on the posts returned from the get_posts function to find
        the correct index.

        """

        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list[Post]:

        """

        get_posts returns the list object containing all posts that have been
        added to the Profile object

        """

        return self._posts

    def make_messages(self, msg_list: list) -> list:

        '''

        uses a list of message dictionaries to create a list of
        Messages following the Messages class

        '''

        list_of_messages = []
        for msg in msg_list:
            new_msg = Messages(msg["message"], msg["from"], msg["timestamp"])
            list_of_messages.append(new_msg)
        return list_of_messages

    def reorganize_message_list(self, msg_list: list) -> dict:

        '''

        Gets a list of Messages and organizes it into a dictionary,
        with the contact as the key.

        '''

        senders_new_old = []

        for msg in msg_list:
            if msg.sender not in senders_new_old:
                senders_new_old.append(msg.sender)

        message_dict = {}

        for sender in senders_new_old:
            message_dict[sender] = []
            for msg in msg_list:
                if msg.sender == sender:
                    message_dict[sender].append(msg)

        return message_dict

    def update_messages(self, all_messages: list) -> None:

        '''

        Locally stores new messages from the server onto a dsu file.

        '''

        msgs_new_old = self.make_messages(all_messages)
        chronological_msgs = self.reorganize_message_list(msgs_new_old)

        for sender in chronological_msgs:
            if sender not in self._messages:
                self._messages[sender] = []
            for msg in chronological_msgs[sender]:
                self._messages[sender].append(msg)

    def save_profile(self, path: str) -> None:

        """

        save_profile accepts an existing dsu file to save the current instance
        of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError

        """

        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding="utf-8") as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Error while attempting to",
                                   "process the DSU file.") from ex
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:

        """

        load_profile will populate the current instance of Profile with
        data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """

        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding="utf-8") as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    for post_obj in obj['_posts']:
                        post = Post(post_obj['entry'], post_obj['timestamp'])
                        self._posts.append(post)

                    for sender_obj in obj['_messages']:
                        sender_msg_list = []
                        for msg in obj['_messages'][sender_obj]:
                            new_msg = Messages(msg['msg'], msg['sender'],
                                               msg['timestamp'])
                            sender_msg_list.append(new_msg)
                        self._messages[sender_obj] = sender_msg_list

            except Exception as ex:
                raise DsuProfileError() from ex
        else:
            raise DsuFileError()
