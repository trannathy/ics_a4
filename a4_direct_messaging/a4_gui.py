'''

A4 takes most of the functionality from previous projects and adds the
DMing messages functionality to it, as well as making it more user friendly by
implememnting a graphical user interface.

'''
from pathlib import Path
from pathlib import WindowsPath
from tkinter import ttk
from tkinter import filedialog
import time
import tkinter as tk

import ds_messenger
import ds_client
import Profile


HOST = "168.235.86.101"
PORT = 3021

USER_DM_BG = "#ffe6ed"
USER_DM_TEXT = "#94475d"
USER_DM_FG = "#d68da2"

CONTACT_DM_BG = "#e0fff2"
CONTACT_DM_TEXT = "#226b4c"
CONTACT_DM_FG = "#96d6bb"


class Body(tk.Frame):

    '''

    The frame responsible for the contact list and message history.

    '''

    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):

        '''

        Command for the contact selection. Selects the
        contact from the tree.

        '''

        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)
        except IndexError:
            pass

    def insert_contact(self, contact: str):

        '''

        Adds a new contact onto the contact tree.
        Called upon receiving a new message from a user or
        when the user manually adds a contact from settings.

        '''

        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

    def _insert_contact_tree(self, contact_id, contact: str):

        '''

        Adds the entire contact tree onto the left side of the body.

        '''

        try:
            if len(contact) > 25:
                entry = contact[:24] + "..."
            contact_id = self.posts_tree.insert('', contact_id,
                                                contact_id,
                                                text=contact)
        except TypeError:
            pass

    def clear_contact_tree(self):

        '''

        Clears the contact list. Called when configuring a new
        account.

        '''

        for contact in self.posts_tree.get_children():
            self.posts_tree.delete(contact)

    def insert_user_message(self, message: str):

        '''

        Adds a new message to the bottom of the chat history
        from the user after the user sends it.

        '''

        self.entry_editor.insert(tk.END, message + '\n', 'user')

    def insert_contact_message(self, message: str):

        '''

        Adds a new message to the bottom of the chat history
        from a contact after the contact sends it.

        '''

        self.entry_editor.insert(tk.END, message + '\n', 'contact')

    def clear_message_history(self):

        '''

        Clears the message history of a chat, used for switching
        contacts or configuring a new account.

        '''

        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:

        '''

        Returns the message that the user typed into the chat box.

        '''

        return self.message_editor.get('1.0', 'end').rstrip()

    def clear_text_entry(self):

        '''

        Clears the chat box. Called after sucessfully sending a message.

        '''

        self.message_editor.delete(1.0, tk.END)

    def clear_all(self):

        '''

        Clears everything in the body. Called for resets.

        '''

        self.clear_contact_tree()
        self.clear_message_history()
        self.clear_text_entry()

    def _draw(self):

        '''

        Sets up all aspects of the body.

        '''

        posts_frame = tk.Frame(master=self, width=250, bg=CONTACT_DM_BG)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        style = ttk.Style()
        style.map('Treeview', background=[('selected', CONTACT_DM_FG)])

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5,
                                      bg=USER_DM_BG)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('user', justify='right',
                                        background=USER_DM_BG,
                                        foreground=USER_DM_TEXT)
        self.entry_editor.tag_configure('contact', justify='left',
                                        background=CONTACT_DM_BG,
                                        foreground=CONTACT_DM_TEXT)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):

    '''

    Creates the footer of the program.

    '''

    def __init__(self, root, send_callback=None, post_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._post_callback = post_callback
        self.config(bg=USER_DM_FG)
        self._draw()

    def send_click(self):

        '''

        Command for the send button. Gets the output of a click on
        the send buttton to send a message.

        '''

        if self._send_callback is not None:
            self._send_callback()

    def post_click(self):

        '''

        Command for the post button. Gets the output of a click on
        the post buttton to send a message.

        '''

        if self._post_callback is not None:
            self._post_callback()

    def _draw(self):

        '''

        Draws everything in the footer.

        '''

        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click,
                                bg=USER_DM_BG)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        post_button = tk.Button(master=self, text="Publish Post",
                                width=20, command=self.post_click,
                                bg=CONTACT_DM_BG)

        post_button.pack(fill=tk.BOTH, side=tk.LEFT, padx=5, pady=5)


class ConfigureDialog(tk.simpledialog.Dialog):

    '''

    Class controlling the dialog box for configure server.

    '''

    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, master):

        '''

        Creates the input boxes for the server, username, and password.

        '''

        self.server_label = tk.Label(master, width=30,
                                     text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(master, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(master, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, width=30, show="*")
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):

        '''

        Gets the entries in the input boxes and sets them as attributes
        of the class instance.

        '''

        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class NewDSUDialog(tk.simpledialog.Dialog):

    '''

    Class controlling the dialog box making a new DSU

    '''

    def __init__(self, root, title=None, user='', pwd='', bio=''):
        self.root = root
        self.user = user
        self.pwd = pwd
        self.bio = bio
        self.server = "168.235.86.101"
        super().__init__(root, title)

    def body(self, master):

        '''

        Creates the input boxes for the server, username, and password.

        '''

        note = "New file to be stored in current directory"
        self.new_dsu_label = tk.Label(master, width=30,
                                      text=note)
        self.new_dsu_label.pack()

        self.username_label = tk.Label(master, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(master, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, width=30, show="*")
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

        self.bio_label = tk.Label(master, width=30, text="Bio (optional)")
        self.bio_label.pack()
        self.bio_entry = tk.Entry(master, width=30)
        self.bio_entry.insert(tk.END, self.bio)
        self.bio_entry.pack()

    def apply(self):

        '''

        Gets the entries in the input boxes and sets them as attributes
        of the class instance.

        '''

        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.bio = self.bio_entry.get()


class MainApp(tk.Frame):

    '''

    Controls the main application/window, holds the body and the footer.

    '''

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = ds_messenger.DirectMessenger()

        self._draw()
        self.configure_server()

    def send_message(self) -> None:

        '''

        Called when the send button in the footer is pressed.
        Tries sending the message in the message box to the contact.
        Clears the text box if successful, or prompts a messagebox to say
        that the mesasge send was not successful.

        '''

        dm_message = self.body.get_text_entry()
        if dm_message.strip() == "":
            send_success = False
        else:
            send_success = self.direct_messenger.send(self.recipient,
                                                      dm_message)
        dm_time = time.time()

        if send_success:
            dm = f'{self.username}, {dm_time}:\n{dm_message}\n'
            self.body.insert_user_message(dm)
            self.body.clear_text_entry()
        else:
            success_title = "MESSAGE UNSUCCESSFUL"
            success_msg = f'ERROR: Message to {self.recipient} not sent.'
            tk.messagebox.showinfo(title=success_title,
                                   message=success_msg)

    def add_contact(self):

        '''

        Command for the add contact button. Promps the user for adding a new
        contact and adds it to the contact tree. This does not save unless
        the contact sends a message to the user.

        '''

        new_friend_prompt = ("Please enter the username of the contact " +
                             "you'd like to add.")
        new_friend = tk.simpledialog.askstring(title="Add Contact",
                                               prompt=new_friend_prompt)

        if new_friend is not None and new_friend.strip() != "":
            self.body.insert_contact(new_friend)

            added_prompt = ("Note: This contact will not save until the " +
                            "user mesasages you back.")
            tk.messagebox.showinfo(title=f"New Contact: {new_friend}",
                                   message=added_prompt)

    def recipient_selected(self, recipient):

        '''

       Command for selection on a contact tree. Loads the chat history
       with the new recipient and clears any leftover text in the message box.

        '''

        self.recipient = recipient
        self.load_message_history()
        self.body.clear_text_entry()

    def format_contact_message(self, msg: dict) -> str:

        '''

        Returns a string with formatting for how messages are displayed
        in the message box.

        '''

        try:
            msg_display = (f'{msg["sender"]}, {msg["timestamp"]}:' +
                           f'\n{msg["msg"]}\n')
        except KeyError:
            msg_display = (f'{msg["from"]}, {msg["timestamp"]}:\n' +
                           f'{msg["message"]}\n')
        return msg_display

    def load_message_history(self) -> None:

        '''

       Gets all the messages from a given recipient from the user's
       dsu file and loads it onto the body.

        '''

        all_msg_hist = self.get_local_messages()
        self.body.clear_message_history()
        try:
            for msg in all_msg_hist[self.recipient]:
                dm = self.format_contact_message(msg)
                self.body.insert_contact_message(dm)

        except KeyError:
            pass

    def update_current_chat(self, new_msgs: list) -> None:

        '''

       Called when the server sends a new message to the user. Checks
       if the new messages are from the contact whose chat the user has open.
       If it is, displays the new message(s)

        '''

        for msg in new_msgs:
            if msg["from"] == self.recipient:
                dm = self.format_contact_message(msg)
                self.body.insert_contact_message(dm)

    def update_contact_list(self, new_msgs: list) -> None:

        '''

       Called when there are new messages for the user. If the user
       does not already have this sender in their contact list, the
       sender is added.

        '''

        for msg in new_msgs:
            if msg["from"] not in self.body._contacts:
                self.body.insert_contact(msg["from"])

    def set_up_gui_new_prof(self):

        '''

        Used to configure the gui for a new account. If the user has not
        sent a dm before, it welcomes them. Otherwise, loads the message
        history of the user.

        '''

        sender_dict = self.get_local_messages()
        if len(sender_dict) == 0:
            pop_msg = ("You have no contacts yet! Add a contact",
                       "using Settings message another user.")
            tk.messagebox.showinfo(title="WELCOME TO DSU DMS!",
                                   message=pop_msg)

        self.body.clear_all()
        for sender in sender_dict:
            self.body.insert_contact(sender)

    def configure_server(self):

        '''

        Gets the information of a new log in attempt. If not canceled and if
        the log in is new from the previously loaded account, prepares to
        set up the gui for the new account.

        '''

        old = (self.username, self.password, self.server)
        new_user = ConfigureDialog(self.root, "Configure Account",
                                   self.username, self.password, self.server)
        new = (new_user.user, new_user.pwd, new_user.server)
        if bool(old != new):
            self.set_up_new_gui(new_user)

    def set_up_new_gui(self, ud: ConfigureDialog):

        '''

        Determines if the log in details are valid. Tries to find the account
        with the log in details. If successful, sets up the new gui for the
        account.
        A log in error prompts the user to re-enter details.

        '''

        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        self.direct_messenger.username = ud.user
        self.direct_messenger.password = ud.pwd
        self.direct_messenger.dsuserver = ud.server

        if self.determine_valid_account(ud.user, ud.pwd, ud.server):
            self.set_up_gui_new_prof()

        else:
            tk.messagebox.showinfo(title="LOGIN ERROR",
                                   message="Invalid Login. Check Details")
            self.configure_server()

    def determine_valid_account(self, user: str, pwd: str, svr: str) -> bool:

        '''

        Returns True or False based on whether the account is valid.
        First tries to to connect to the server. If joining is successful,
        returns true If this account have never been logged into on the
        device, creates a new dsu file for it.
        If joining is not successful, checks if the account has an offline
        backup dsu file for it. Returns true and loads messages offline if
        it does, returns false otherwise.

        '''

        empty = any(len(ele.strip()) == 0 for ele in [user, pwd, svr])

        if empty:
            return False

        join_success = ds_client.send(svr, PORT, user, pwd, "")

        if join_success is False:
            valid_login = self.check_offline(user, pwd, svr)
            if valid_login:
                tk.messagebox.showinfo(title="NO CONNECTION",
                                       message="Loading Messages Offline")
                return True

            return False
        dsu_path = Path(self.get_dsu_path_user(user))

        if not dsu_path.exists():
            self.create_new_dsu_file(svr, user, pwd, dsu_path)

        self.dm_local_save(dsu_path)

        return True

    def create_new_dsu_file(self, dsuserver, username, password,
                            file_path: WindowsPath, bio=None) -> None:

        '''

        Creates a new dsu file for an account the device has not accessed
        before.

        '''

        file_path.touch()
        new_prof = Profile.Profile(dsuserver, username, password)
        if bio is not None:
            new_prof.bio = bio
        print(f"\n{str(file_path)} CREATED\n")
        new_prof.save_profile(file_path)

    def dm_local_save(self, file_path: WindowsPath, msg_list=None) -> None:

        '''

        Saves messages locally onto the dsu file.

        '''

        get_new_only = bool(len(self.get_local_messages()) == 0)

        load_true = self.direct_messenger.save_dms_local(str(file_path),
                                                         get_new_only,
                                                         msg_list)

        if load_true is False:
            tk.messagebox.showinfo(title="CONNECTION LOST",
                                   message="Please Reconnect")

    def get_local_messages(self) -> dict:

        '''

        Gets the dictionary of messages and their senders from the
        offline backup.

        '''

        dsu_path = Path(self.get_dsu_path_user(self.username))
        prof = Profile.Profile()
        prof.load_profile(dsu_path)
        message_dict = prof._messages
        return message_dict

    def check_offline(self, username: str, password: str, server: str) -> bool:

        '''

        If connection to the server was unsuccessful, checks if the login
        details matches any stored locally.

        '''

        test_path = self.get_dsu_path_user(username)

        if not Path(test_path).exists():
            return False
        return self.check_login_offline(test_path, password, server)

    def get_dsu_path_user(self, username: str) -> str:

        '''

        Gets the path of the dsu file for a specified user.

        '''

        directory = Path(".")
        file_name = Path(username + ".dsu")
        path = directory / file_name
        return str(path)

    def check_login_offline(self, offline_path: str, pwd_test: str,
                            svr_test: str) -> bool:

        '''

        Cross references the provided login details from the user and the
        ones stored within offline backup.

        '''

        prof = Profile.Profile()
        prof.load_profile(offline_path)
        return bool((prof.password == pwd_test) and
                    (prof.dsuserver == svr_test))

    def publish(self) -> None:

        '''

        Publishes a post and bio onto the web.

        '''

        entry = tk.simpledialog.askstring(title="New Post",
                                          prompt="Enter a message to post:")

        try:
            prof = Profile.Profile()
            path = self.get_dsu_path_user(self.username)
            prof.load_profile(path)

            if entry is not None and entry.strip() != "":
                post_success = ds_client.send(self.server, PORT, self.username,
                                              self.password, entry, prof.bio)
                if post_success:
                    tk.messagebox.showinfo(message="Posted!")
                else:
                    tk.messagebox.showinfo(message="Message Not Posted.")
            elif entry is not None:
                tk.messagebox.showinfo(message="Invalid entry")
        except Profile.DsuFileError:
            tk.messagebox.showinfo(message="Profile Not Found")

    def new_dsu_set_attributes(self, dsu: NewDSUDialog) -> None:

        '''

        Sets the attributes of the application to be the ones specified
        in the making of the new DSU.

        '''

        self.username = dsu.user
        self.password = dsu.pwd
        self.server = dsu.server

        self.direct_messenger.username = dsu.user
        self.direct_messenger.password = dsu.pwd
        self.direct_messenger.dsuserver = dsu.server

    def existing_dsu_set_attributes(self, dsu_path) -> None:

        '''

        If the DSU already exists, sets the the application attributes
        to the attributes of the existing file.

        '''

        prof = Profile.Profile()
        prof.load_profile(dsu_path)

        self.username = prof.username
        self.password = prof.password
        self.server = prof.dsuserver

        self.direct_messenger.username = prof.username
        self.direct_messenger.password = prof.password
        self.direct_messenger.dsuserver = prof.dsuserver

    def existing_dsu_update(self, new_dsu: NewDSUDialog, path: str) -> bool:

        '''

        If the dsu already exists, sets attributes to match with it.
        Additionality, if a new bio is provided, changes it within the DSU

        '''

        prof = Profile.Profile()
        prof.load_profile(path)

        if prof.password != new_dsu.pwd:
            return False

        self.new_dsu_set_attributes(new_dsu)

        if new_dsu.bio.strip() != "":
            prof.bio = new_dsu.bio
            prof.save_profile(path)

        return True

    def new_dsu_option(self):

        '''

        Command for DSU Files > New DSU File.
        Allows the user to name a DSU file, if it is a valid
        login. Opens the file if it already exists.

        '''

        old = (self.username, self.password, self.server)

        dsu = NewDSUDialog(self.root, "New DSU")
        dsu_path = self.get_dsu_path_user(dsu.user)

        new = (dsu.user, dsu.pwd, dsu.server)

        if old == new:
            pass

        elif Path(dsu_path).exists():
            if self.existing_dsu_update(dsu, dsu_path):
                out_msg = ("DSU File already exists." +
                           "\nLoading existing file.")
                self.set_up_gui_new_prof()
            else:
                out_msg = ("ERROR: DSU File already exists." +
                           "\nProvided login details incorrect.")
            tk.messagebox.showinfo(title="File Already Exists",
                                   message=out_msg)

        elif ds_client.send(dsu.server, PORT, dsu.user, dsu.pwd, ""):
            self.new_dsu_set_attributes(dsu)
            if dsu.bio.strip() != "":
                bio_add = dsu.bio
            else:
                bio_add = None
            self.create_new_dsu_file(self.server, self.username,
                                     self.password, Path(dsu_path), bio_add)
            self.set_up_gui_new_prof()

    def open_dsu_option(self):

        '''

        Command for DSU Files > Open DSU File.
        Allows the user to open a DSU File.

        '''
        directory_str = str(Path("."))

        file_path = filedialog.askopenfilename(initialdir=directory_str)

        if file_path.endswith(".dsu") and (directory_str in file_path):
            self.existing_dsu_set_attributes(file_path)
            self.set_up_gui_new_prof()
        elif file_path.strip() != "":
            tk.messagebox.showinfo(title="File Error",
                                   message="Invalid DSU File.")

    def close_dsu_option(self):

        '''

        Command for DSU Files > Close DSU File.
        Resets the program. Clears all data.

        '''

        self.username = ''
        self.password = ''
        self.server = ''
        self.recipient = ''
        self.direct_messenger = ds_messenger.DirectMessenger()
        self.body.clear_all()

    def check_new(self):

        '''

        Checks for new messages incoming to the user. Retuns repeatedly
        throughout the program.

        '''

        new_msgs = self.direct_messenger.retrieve_new(False)
        if new_msgs is not None and len(new_msgs) > 0:
            dsu_file = self.get_dsu_path_user(self.username)
            self.dm_local_save(dsu_file, new_msgs)
            self.update_current_chat(new_msgs)
            self.update_contact_list(new_msgs)
        main.after(2000, self.check_new)

    def _draw(self):

        '''

        Builds the application

        '''

        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='DSU Files')
        menu_file.add_command(label='New DSU File',
                              command=self.new_dsu_option)
        menu_file.add_command(label='Open DSU FIle',
                              command=self.open_dsu_option)
        menu_file.add_command(label='Close DSU File',
                              command=self.close_dsu_option)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message,
                             post_callback=self.publish)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":

    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id_after = main.after(2000, app.check_new)
    print(id_after)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
