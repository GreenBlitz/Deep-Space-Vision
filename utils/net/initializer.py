from networktables import NetworkTables
import os

NetworkTables.initialize('10.45.90.20')


sd = NetworkTables.getTable('SmartDashboard')

NetworkTables.create()

sd.putString('bash_command', 'la')

key_commands = { # dict of lists of callback functions
    'bash_command': [
        lambda value, is_new: os.system(value)
    ]
}


def add_on_entry_change(key, func):
    if key not in key_commands:
        key_commands[key] = []
    key_commands[key].append(func)


def set_smart_dashboard_value(key, value):
    pass # TODO create this function


def entry_change_callback(key, value, is_new):
    for i in key_commands[key]:
        i(value, is_new)


print(sd.getNumber('robot y', 'did not fucking work fuck everyone and especially fucking motion'))
