from networktables import NetworkTables
from net_consts import *
import os


def initialize_values():
    global key_commands
    global vision_table

    NetworkTables.initialize(NETWORK_TABLE_IP)
    vision_table = NetworkTables.getTable(VISION_TABLE_NAME)

    key_commands = {  # dict of lists of callback functions
        'bash_command': [
            lambda value, is_new: os.system(value)
        ]
    }


def add_on_entry_change(key, func):
    if key not in key_commands:
        key_commands[key] = []
    key_commands[key].append(func)


def set_network_table_value(key, value):

    pass # TODO create this function


def __entry_change_callback(key, value, is_new):
    for i in key_commands[key]:
        i(value, is_new)

