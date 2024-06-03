'''

ui.py contains UI commands for the program, including all the menus.

'''

# THY TRAN
# THYNT1@UCI.EDU
# 90526048

OUTPUT_NOT_DSU = "\nERROR: FILE IS NOT A DSU\n"
OUTPUT_NO_PERM = "\nERROR: PERMISSION FOR ACTION DENIED\n"
OUTPUT_NO_PATH = "\nERROR: PATH INVALID\n"
OUTPUT_D_R_O_USE = "\nERROR: D, R, O COMMANDS SHOULD BE FOLLOWED BY A PATH\n"
OUTPUT_C_USE = "\nERROR: C FORMAT: C [PATH] -n [NEW_DSU_NAME]\n"
OUTPUT_FILE_EXISTS = "\nFILE ALREADY EXISTS, OPENING FILE\n"

OUTPUT_COMMAND_INVALID = "\nERROR: COMMAND INVALID\n"
OUTPUT_E_OPTION_INVALID = "\nERROR: NOT A VALID EDIT OPTION\n"
OUTPUT_ID_INVALID = "\nERROR: POST ID NOT AN INT\n"
OUTPUT_INDEX_ERROR = "\nERROR: INVALID ID, OUT OF RANGE\n"
OUTPUT_ID_NEGATIVE = "\nERROR: ID CANNOT BE NEGATIVE\n"
OUTPUT_E_USE = "\nERROR: E COMMAND MUST BE FOLLOWED BY OPTIONS\n"
OUTPUT_POST_USE = "\nERROR: -post OPTION MUST BE FOLLOWED BY ID\n"
OUTPUT_DUPLICATE = "\nDUPLICATE COMMAND; IGNORING PREVIOUS "
OUTPUT_EMPTY_COMMAND = "COMMAND SKIPPED, EMPTY INPUT\n"


def welcome():

    '''

    Prints an initial welcome message, used for start of the program

    '''

    print("Welcome to the DSU file explorer!")


def command_intake_ui(mode) -> str:

    '''

    Contains the main command menu for creating, deleting, opening,
    or reading a dsu file. Returns just a newline if in admin mode.

    '''

    if not mode:
        return ("COMMAND MENU:" +
                "\n[COMMAND] - What the command does" +
                "\n----------------------------------" +
                "\nC - Create a new file in the specified directory" +
                "\n\t-n (new_file_name)"
                "\nO - Open an existing file of type dsu"
                "\nR - Read the contents of a file." +
                "\nD - Delete the file." +
                "\nQ - Quit" +
                "\nPlease input your command in the correct format:" +
                "\n[COMMAND] [PATH] ([[-n]OPTION] [INPUT])\n"
                )

    return "\n"


def opened_file_ui(directory: str, mode: bool) -> str:

    '''

    Contains the menu for an opened file, including editing, printing,
    publishing, and closing the file. Returns just a newline if in admin mode

    '''

    if not mode:
        return ("COMMAND MENU FOR " + directory +
                f'\n{"E - Edit Options":20}|{"P - Print Options":20}' +
                f'\n{"-usr [USERNAME]":20}|{"-usr":20}' +
                f'\n{"-pwd [PASSWORD]":20}|{"-pwd":20}' +
                f'\n{"-bio [BIO]":20}|{"-bio":20}' +
                f'\n{"-addpost [NEW POST]":20}|{"-posts":20}' +
                f'\n{"-delpost [ID]":20}|{"-post [ID]":20}' +
                f'\n{" ":20}|{"-all":20}' +
                "\nPUB_POST [ID] - Publishes a post entry onto DSU server"
                "\nPUB_BIO - Publishes a new bio onto the DSU server"
                '\nCL - Close file, enter main commands\n' +
                "\nPlease input your command in the correct format:" +
                "\n[COMMAND] [[-]OPTION] [INPUT]\n")

    return "\n"


def set_new_profile(new_attribute: str, mode):

    '''

    Contains the instructions for setting up a new dsu profile.
    Returns just a newline if in admin mode.

    '''

    if not mode:
        if new_attribute == "bio":
            optional = "OPTIONAL: "
        else:
            optional = ""
        return (optional +
                f"\nPlease enter a new {new_attribute} for your profile:\n")

    return "\n"
