from networktables import NetworkTables
from net_consts import *
import os

vision_table = None
__key_commands = None


def net_init():
    """
    initializes all network values
    """
    global vision_table
    global __key_commands
    NetworkTables.initialize(NETWORK_TABLES_IP)

    vision_table = NetworkTables.getTable(VISION_TABLE_NAME)

    __key_commands = {  # dict of lists of callback functions
        'bash_command': [
            lambda value, is_new: os.system(value)
        ]
    }

    vision_table.addEntryListener(__entry_change_callback)


def add_on_entry_change(key, func):
    """
    add a function to be called every time a specific entry is changed on the vision table
    :param key
    :param func:
    """
    if hasattr(key, "__iter__"):
        for k in key:
            add_on_entry_change(k, func)
    if key not in __key_commands:
        __key_commands[key] = []
    __key_commands[key].append(func)


def __entry_change_callback(key, value, is_new):
    """
    runs when an entry is changed on the vision table
    :param key:
    :param value:
    :param is_new:
    """
    for i in __key_commands[key]:
        try:
            i(value)
        except TypeError:
            i(value, is_new)


# fuck git
