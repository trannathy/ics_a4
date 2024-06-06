import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
import ds_messenger
import ds_client
from pathlib import Path
from pathlib import WindowsPath
import Profile
import time

PORT = 3021
USER_DM_BG = "#ffe6ed"
USER_DM_TEXT = "#94475d"
USER_DM_FG = "#d68da2"

CONTACT_DM_BG = "#e0fff2"
CONTACT_DM_TEXT = "#226b4c"
CONTACT_DM_FG = "#96d6bb"


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)
        except IndexError:
            pass

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        try:
            if len(contact) > 25:
                entry = contact[:24] + "..."
            id = self.posts_tree.insert('', id, id, text=contact)
        except TypeError:
            pass

    def clear_contact_tree(self):
        for contact in self.posts_tree.get_children():
            self.posts_tree.delete(contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'user')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(tk.END, message + '\n', 'contact')

    def clear_message_history(self):
        self.entry_editor.delete(1.0, tk.END)

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def clear_text_entry(self):
        self.message_editor.delete(1.0, tk.END)

    def clear_all(self):
        self.clear_contact_tree()
        self.clear_message_history()
        self.clear_text_entry()

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250, bg = CONTACT_DM_BG)
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
                                      bg = USER_DM_BG)
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
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self.config(bg=USER_DM_FG)
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send",
                                width=20, command=self.send_click,
                                bg=USER_DM_BG)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, self.server)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, self.user)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.insert(tk.END, self.pwd)
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
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

    def send_message(self):
        dm_message = self.body.get_text_entry()
        send_success = self.direct_messenger.send(self.recipient, dm_message)
        dm_time = time.time()

        if send_success:
            dm = f'{self.username}, {dm_time}:\n{dm_message}\n'
            self.body.insert_user_message(dm)
            self.body.clear_text_entry()
        else:
            success_title = "MESSAGE UNSUCCESSFUL"
            success_msg = f'ERROR: Message to {self.recipient} not sent.'
            tk.messagebox.showinfo(title = success_title,
                                   message = success_msg)
    

    def add_contact(self):
        new_friend_prompt = ("Please enter the username of the contact " +
                             "you'd like to add.")
        new_friend = tk.simpledialog.askstring(title="Add Contact",
                                                prompt=new_friend_prompt)
        self.body.insert_contact(new_friend)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.load_message_history()

    def format_contact_message(self, msg: dict) -> str:
        try:
            msg_display = f'{msg["sender"]}, {msg["timestamp"]}:\n{msg["msg"]}\n'
        except KeyError:
            msg_display = (f'{msg["from"]}, {msg["timestamp"]}:\n' +
                           f'{msg["message"]}\n')
        return msg_display
    
    def load_message_history(self) -> None:
        all_msg_hist = self.get_local_messages()
        self.body.clear_message_history()
        try:
            for msg in all_msg_hist[self.recipient]:
                dm = self.format_contact_message(msg)
                self.body.insert_contact_message(dm)

        except KeyError:
            pass

    def update_current_chat(self, new_msgs: list) -> None:
        for msg in new_msgs:
            if msg["from"] == self.recipient:
                dm = self.format_contact_message(msg)
                self.body.insert_contact_message(dm)
    
    def set_up_gui_new_prof(self):
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
        new_user = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        
        self.set_up_new_gui(new_user)

    def set_up_new_gui(self, ud: NewContactDialog):
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server

        self.direct_messenger.username = ud.user
        self.direct_messenger.password = ud.pwd
        self.direct_messenger.dsuserver = ud.server

        if self.determine_valid_account(ud.user, ud.pwd, ud.server):
            self.set_up_gui_new_prof()
            
        else:
            tk.messagebox.showinfo(title = "LOGIN ERROR",
                                   message = "Invalid Login. Check Details")
            self.configure_server()

    def determine_valid_account(self, user: str, pwd: str, svr: str) -> bool:
        empty = any(len(ele.strip()) == 0 for ele in [user, pwd, svr])

        if empty:
            return False
        
        join_success = ds_client.send(svr, PORT, user, pwd, "")

        if join_success is False:
            valid_login = self.check_offline(user, pwd)
            if valid_login:
                tk.messagebox.showinfo(title = "NO CONNECTION",
                                   message = "Loading Messages Offline")
                return True
    
            return False
        dsu_path = Path(self.get_dsu_path_user(user))

        if not dsu_path.exists():
            self.create_new_dsu_file(svr, user, pwd, dsu_path)

        self.dm_local_save(dsu_path)

        return True
    
    def create_new_dsu_file(self, dsuserver, username, password,
                            file_path: WindowsPath) -> None:
        file_path.touch()
        new_prof = Profile.Profile(dsuserver, username, password)
        print(f"\n{str(file_path)} CREATED\n")
        new_prof.save_profile(file_path)

    def dm_local_save(self, file_path: WindowsPath, msg_list=None) -> None:
        if len(self.get_local_messages()) == 0:
            get_new_only = True
        else: 
            get_new_only = False
        load_true = self.direct_messenger.save_dms_local(str(file_path),
                                                         get_new_only,
                                                         msg_list)

        if load_true is False :
            tk.messagebox.showinfo(title = "CONNECTION LOST",
                                   message = "Please Reconnect")

    def get_local_messages(self) -> dict:
        dsu_path = Path(self.get_dsu_path_user(self.username))
        prof = Profile.Profile()
        prof.load_profile(dsu_path)
        message_dict = prof._messages
        return message_dict

    def check_offline(self, username: str, password: str) -> bool:
        test_path = self.get_dsu_path_user(username)

        if not Path(test_path).exists():
            return False
        return self.check_password_offline(test_path, password)
    
    def get_dsu_path_user(self, username: str) -> str:
        directory = Path(".")
        file_name = Path(username + ".dsu")
        path = directory / file_name
        return str(path)

    def check_password_offline(self, offline_path, pwd_test) -> bool:
        prof = Profile.Profile()
        prof.load_profile(offline_path)
        return bool(prof.password == pwd_test)

    def publish(self, message:str):
        # You must implement this!
        pass

    def check_new(self):
        new_msgs = self.direct_messenger.retrieve_new(False)
        if new_msgs is not None and len(new_msgs) > 0:
            dsu_file = self.get_dsu_path_user(self.username)
            self.dm_local_save(dsu_file, new_msgs)
            self.update_current_chat(new_msgs)
        main.after(2000, self.check_new)

    def _draw(self):
        # Build a menu and add it to the root frame.

        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='DSU Files')
        menu_file.add_command(label='New DSU File')
        menu_file.add_command(label='Open DSU FIle')
        menu_file.add_command(label='Close DSU File')

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
        self.footer = Footer(self.root, send_callback=self.send_message)
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
    id = main.after(2000, app.check_new)
    print(id)
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
