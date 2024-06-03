'''

A3: DSU profiles with DSU Server Integration
This is where the user interacts with the program to create, edit, view, and
delete DSU files.

'''

# THY TRAN
# THYNT1@UCI.EDU
# 90526048

import shlex
import os
from pathlib import Path
from pathlib import WindowsPath

import ds_client
import Profile
import ui


HOST = "168.235.86.101"
PORT = 3021


class Editing:

    '''

    Stores commands for making edits to a profile's username, password, or bio.
    Also informs the user of changes made.

    '''

    def __init__(self, attribute, attribute_edit, profile_path) -> None:

        '''

        constructs the Edit with the attribute to be edited, its new value,
        and the path of the profile.

        '''

        self.attribute = attribute
        self.attribute_edit = attribute_edit
        self.profile_path = profile_path

    def make_edit(self) -> None:

        '''

        Makes an edit to the profile based on what the attribute is.
        Informs the user if there is no change made.

        '''

        prof = Profile.Profile()
        prof.load_profile(self.profile_path)

        if self.attribute == "USERNAME":
            old = self.edit_user(prof)

        elif self.attribute == "PASSWORD":
            old = self.edit_pwd(prof)

        else:
            old = self.edit_bio(prof)

        if old == self.attribute_edit:
            print(f"{self.attribute} IS ALREADY {self.attribute_edit}" +
                  "\nNO CHANGE MADE\n")

        else:
            print(f"OLD {self.attribute}: {old}")
            print(f"NEW {self.attribute}: {self.attribute_edit}\n")

        prof.save_profile(self.profile_path)

    def edit_user(self, profile: Profile.Profile) -> str:

        '''

        Edits a username and returns the old username.

        '''

        old_attribute = profile.username
        profile.username = self.attribute_edit
        return old_attribute

    def edit_pwd(self, profile: Profile.Profile) -> str:

        '''

        Edits a password and returns the old password.

        '''

        old_attribute = profile.password
        profile.password = self.attribute_edit
        return old_attribute

    def edit_bio(self, profile: Profile.Profile) -> str:

        '''

        Edits a bio and returns the old bio.

        '''

        old_attribute = profile.bio
        profile.bio = self.attribute_edit
        return old_attribute


class FileCommands:

    '''

    Stores all the the commands for when a file is Loaded.

    '''

    def check_id(self, post_id: str) -> bool:

        '''

        Ensures that any post ID that the user requests is a non-negative
        integer

        '''

        try:
            int_id = int(post_id)
            if int_id < 0:
                print(ui.OUTPUT_ID_NEGATIVE)
                return False
            return True

        except ValueError:
            print(ui.OUTPUT_ID_INVALID)
            return False

    def file_command_intake(self, path: str, mode: bool) -> str:

        '''

        Gets a command from the user

        '''

        user_input = input(ui.opened_file_ui(path, mode))
        return user_input

    def file_command_check_validity(self, command_line) -> bool:

        '''

        Makes sure that the user command is an option

        '''

        if command_line[0] == "E" and len(command_line) % 2 == 1:
            return self.edit_command_check_validity(command_line)

        if command_line[0] == "P" and len(command_line) > 1:
            return self.print_command_check_validity(command_line)

        if command_line[0] == "PUB_POST" and len(command_line) == 2:
            return self.publish_command_check_validity(command_line)

        if command_line[0] == "PUB_BIO" and len(command_line) == 1:
            return True

        print(ui.OUTPUT_COMMAND_INVALID)
        return False

    def edit_command_check_validity(self, command_line) -> bool:

        '''

        Makes sure that an edit command follows input structure.

        '''

        option_list = ["-usr", "-pwd", "-bio", "-addpost", "-delpost"]
        options = command_line[1:]

        if len(options) == 0:
            print(ui.OUTPUT_E_USE)
            return False

        for index, option in enumerate(options):
            if (index % 2 == 0) and (option not in option_list):
                print(ui.OUTPUT_E_OPTION_INVALID)
                return False

            if (index % 2 == 0 and (option == "-delpost" and
                                    not self.check_id(options[index + 1]))):
                return False

        return True

    def print_command_check_validity(self, command_line) -> bool:

        '''

        Makes sure that a print command follows input structure.

        '''

        option_list = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]
        options = command_line[1:]

        if options[-1] == "-post":
            print(ui.OUTPUT_POST_USE)
            return False

        for index, option in enumerate(options):
            if option not in option_list and options[index - 1] == "-post":
                if not self.check_id(option):
                    break

            elif option not in option_list and options[index - 1] != "-post":
                print(ui.OUTPUT_COMMAND_INVALID)
                return False

            elif option == "-post" and not self.check_id(options[index + 1]):
                return False

        return True

    def publish_command_check_validity(self, command_line) -> bool:

        '''

        Makes sure that a publish command has a valid id.

        '''

        return self.check_id(command_line[1])

    def get_edits(self, command_line) -> tuple:

        '''

        Retrieves edits options from a command, removing duplicates

        '''

        options = command_line[1:]
        commands = []
        edits = []

        for ind, command in enumerate(options):
            if ind % 2 == 0 and (command not in commands or
                                 command == "-addpost"):
                commands.append(command)

            elif ind % 2 == 0 and command in commands:
                print(f"{ui.OUTPUT_DUPLICATE} {command}\n")

                prev_command_ind = commands.index(command)
                commands.remove(command)
                edits.remove(edits[prev_command_ind])

                commands.append(command)

            else:
                edits.append(command)

        return commands, edits

    def edit_user(self, new_user, dsu_path) -> None:

        '''

        Initiates username edit

        '''

        username_edit = Editing("USERNAME", new_user, dsu_path)
        username_edit.make_edit()

    def edit_pwd(self, new_pwd, dsu_path) -> None:

        '''

        Initiates password edit

        '''

        password_edit = Editing("PASSWORD", new_pwd, dsu_path)
        password_edit.make_edit()

    def edit_bio(self, new_bio, dsu_path) -> None:

        '''

        Initiates bio edit

        '''

        bio_edit = Editing("BIO", new_bio, dsu_path)
        bio_edit.make_edit()

    def edit_addpost(self, new_entry, dsu_path) -> None:

        '''

        Creates a post and prints it to the user.

        '''

        new_post = Profile.Post()
        new_post.set_entry(new_entry)

        profile = Profile.Profile()
        profile.load_profile(dsu_path)

        profile.add_post(new_post)

        all_posts = profile.get_posts()
        post_id = len(all_posts) - 1

        print("NEW POST SUCCESSFULLY ADDED:")
        self.print_post(all_posts, post_id)

        profile.save_profile(dsu_path)

    def edit_delpost(self, post_to_delete: int, dsu_path: str) -> None:

        '''

        Deletes a post, identifed by its id

        '''

        profile = Profile.Profile()
        profile.load_profile(dsu_path)

        deletion = profile.del_post(post_to_delete)

        if deletion:
            print(f"\nPOST {post_to_delete} DELETED\n")
            profile.save_profile(dsu_path)

        else:
            print(ui.OUTPUT_INDEX_ERROR)

    def get_prints(self, command_line) -> tuple:

        '''

        Retrieves print options from a command, removing duplicates

        '''

        command_list = ["-usr", "-pwd", "-bio", "-posts", "-post", "-all"]
        command_line = command_line[1:]

        all_commands = []
        post_id = None

        for index, command in enumerate(command_line):
            if command == "-post":
                all_commands. append(command)

            elif command in command_list and command not in all_commands:
                all_commands.append(command)

            elif command_line[index - 1] == "-post":
                post_id = int(command)

        if "-all" in all_commands:
            all_commands = ["-usr", "-pwd", "-bio", "-posts"]

        return all_commands, post_id

    def print_all_posts(self, posts: list[Profile.Post]) -> None:

        '''

        Prints all posts on a profile, or NO POST if none

        '''

        if len(posts) == 0:
            print("NO POSTS")

        else:
            for i in range(len(posts)):
                self.print_post(posts, i)
                i += 1

    def print_post(self, posts: list[Profile.Post], post_id: int) -> None:

        '''

        Prints a post identified by its id

        '''

        print("\nID: " + str(post_id))
        print("ENTRY:")
        print(posts[post_id].get_entry())
        print("TIMESTAMP:")
        print(str(posts[post_id].get_time()) + "\n")

    def edit_file(self, command_list: list[str], path: str) -> None:

        '''

        Loops through all edit options to edit a file

        '''

        attributes, new_att = self.get_edits(command_list)

        for index, attribute in enumerate(attributes):
            if check_empty(new_att[index]):
                print(f"\n{attribute} {ui.OUTPUT_EMPTY_COMMAND}")

            elif attribute == "-usr":
                self.edit_user(new_att[index], path)

            elif attribute == "-pwd":
                self.edit_pwd(new_att[index], path)

            elif attribute == "-bio":
                self.edit_bio(new_att[index], path)

            elif attribute == "-addpost":
                self.edit_addpost(new_att[index], path)

            elif attribute == "-delpost":
                self.edit_delpost(int(new_att[index]), path)

    def print_file(self, command_list: list[str], path: str) -> None:

        '''

        Loops through all print options to print a file's contents

        '''

        print_commands, read_id = self.get_prints(command_list)

        prof = Profile.Profile()
        prof.load_profile(path)
        posts_list = prof.get_posts()

        if read_id is not None and read_id > (len(posts_list) - 1):
            print(ui.OUTPUT_INDEX_ERROR)

        else:
            for command in print_commands:
                if command == "-usr":
                    print(f"USERNAME: {prof.username}")

                elif command == "-pwd":
                    print(f"PASSWORD: {prof.password}")

                elif command == "-bio":
                    print(f"BIO: {prof.bio}")

                elif command == "-posts":
                    self.print_all_posts(posts_list)

                elif command == "-post":
                    self.print_post(posts_list, read_id)

    def publish_post(self, command_list: list[str], path: str):

        '''

        Sends a request to publish a post onto the DSU server

        '''

        prof = Profile.Profile()
        prof.load_profile(path)

        posts_list = prof.get_posts()

        post_id = int(command_list[1])

        try:
            post_to_pub = posts_list[post_id].get_entry()
            send_success = ds_client.send(HOST, PORT, prof.username,
                                          prof.password, post_to_pub)
            print(f"PUBLISH BIO SUCCESSFUL: {send_success}\n")

        except IndexError:
            print(ui.OUTPUT_INDEX_ERROR)

    def publish_bio(self, path: str) -> None:

        '''

        Sends a request to publish a bio onto the DSU server

        '''

        prof = Profile.Profile()
        prof.load_profile(path)
        send_success = ds_client.send(HOST, PORT, prof.username,
                                      prof.password, "", prof.bio)

        print(f"PUBLISH BIO SUCCESSFUL: {send_success}\n")

    def file_run(self, path: str, mode: bool) -> None:

        '''

        Asks for file commands and runs them

        '''

        file_command = self.file_command_intake(path, mode)

        if file_command.strip() != "CL":

            try:
                file_command = shlex.split(file_command)

            except ValueError:
                print(ui.OUTPUT_COMMAND_INVALID)
                self.file_run(path, mode)

            else:
                if self.file_command_check_validity(file_command) is False:
                    pass

                elif file_command[0] == "E":
                    self.edit_file(file_command, path)

                elif file_command[0] == "P":
                    self.print_file(file_command, path)

                elif file_command[0] == "PUB_POST":
                    self.publish_post(file_command, path)

                elif file_command[0] == "PUB_BIO":
                    self.publish_bio(path)

                self.file_run(path, mode)


def create_file(command_line: list, admin) -> None:

    '''

    Creates a new dsu file according to the user's path and name inputs,
    or opens a dsu file if it already exists.

    '''

    directory = Path(command_line[1])
    file_name = Path(command_line[3] + ".dsu")
    path = directory / file_name

    if path.exists():
        print(ui.OUTPUT_FILE_EXISTS)
        open_file(["O", str(path)], admin)

    else:
        try:
            path.touch()
            path.unlink()

        except FileNotFoundError:
            print(ui.OUTPUT_NO_PATH)

        else:
            make_new_file(path, admin)


def open_file(command_line, admin) -> None:

    '''

    Loads a dsu file if it exists and opens the file command menu.

    '''

    if check_dsu(command_line):
        path = Path(command_line[-1])

        if path.exists():

            with open(path, "a+", encoding="utf-8"):
                print(f"\n{str(path)} SUCESSFULLY LOADED\n")
                file_commands = FileCommands()
                file_commands.file_run(str(path), admin)

            print(f"\n{str(path)} CLOSED\n")

        else:
            print(ui.OUTPUT_NO_PATH)

    else:
        print(ui.OUTPUT_NOT_DSU)


def delete_file(command_line) -> None:

    '''

    Deletes a file if it is a dsu and exists.

    '''

    if check_dsu(command_line):
        path = Path(command_line[-1])

        path.unlink()
        print(f"\n{path} DELETED\n")

    else:
        print(ui.OUTPUT_NOT_DSU)


def read_file(command_line) -> None:

    '''

    Reads all the line of text in a dsu file, or "EMPTY" if there is no text.

    '''

    if check_dsu(command_line):
        path = Path(command_line[-1])

        if os.path.getsize(path) == 0:
            print('EMPTY')
        else:
            print(path.read_text(encoding="utf-8"))

    else:
        print(ui.OUTPUT_NOT_DSU)


def command_intake(mode) -> str:

    '''

    Asks the user for inputs for a command, with a menu if not in admin mode

    '''

    user_input = input(ui.command_intake_ui(mode))
    return user_input


def profile_set_up(mode) -> tuple:

    '''

    Asks the user to specify a username, password, and optional bio
    for a newly created profile.

    '''

    user = ""
    while check_empty(user):
        user = input(ui.set_new_profile("username", mode))

    pwd = ""
    while check_empty(pwd):
        pwd = input(ui.set_new_profile("password", mode))

    bio = input(ui.set_new_profile("bio", mode))

    return user, pwd, bio


def make_new_file(file_path: WindowsPath, mode) -> None:

    '''

    Creates a new profile and loads it onto a dsu file based on user-specified
    information.

    '''

    new_username, new_password, new_bio = profile_set_up(mode)
    new_profile = Profile.Profile(dsuserver="168.235.86.101",
                                  username=new_username, password=new_password)
    new_profile.bio = new_bio

    file_path.touch()
    print(f"\n{str(file_path)} CREATED\n")
    new_profile.save_profile(file_path)

    open_file(["O", str(file_path)], mode)


def check_validity(command_line):

    '''

    Checks if the user command follows the specified format.

    '''

    command = command_line[0]

    if command in ['D', 'R', 'O'] and len(command_line) == 2:
        return True

    if command in ['D', 'R', 'O'] and len(command_line) != 2:
        print(ui.OUTPUT_D_R_O_USE)
        return False

    if (command == 'C' and len(command_line) == 4 and
            command_line[2] == "-n"):
        return True

    if command == 'C' and (len(command_line) != 4 or
                           command_line[2] != "-n"):
        print(ui.OUTPUT_C_USE)
        return False

    print(ui.OUTPUT_COMMAND_INVALID)
    return False


def check_path(command_line):

    '''

    Checks if user specified path exists.

    '''

    path = Path(command_line[1])

    if not path.exists():
        print(ui.OUTPUT_NO_PATH)
        return False

    return True


def check_dsu(command_line: list[str]):

    '''

    Checks if a file is a dsu.

    '''

    path_str = command_line[-1]

    return bool(path_str.endswith(".dsu"))


def check_empty(str_input: str) -> bool:

    '''

    Checks if a string input is empty or just whitespace.

    '''

    return bool(str_input.strip() == "")


def run(mode: bool):

    '''

    Entry point into the program, used to faciliate creating, opening,
    deleting, or reading a file.

    '''

    user_command = command_intake(mode)

    if user_command == 'admin':
        run(not mode)

    elif user_command != "Q":
        try:
            user_command = shlex.split(user_command)

        except ValueError:
            print(ui.OUTPUT_COMMAND_INVALID)
            run(mode)

        else:
            if (check_validity(user_command) is False or
                    check_path(user_command) is False):
                pass

            elif user_command[0] == 'C':
                create_file(user_command, mode)

            elif user_command[0] == 'O':
                open_file(user_command, mode)

            elif user_command[0] == 'D':
                delete_file(user_command)

            elif user_command[0] == 'R':
                read_file(user_command)

            run(mode)


if __name__ == "__main__":
    ui.welcome()
    run(False)
