from networktables import NetworkTables

from .net_consts import *

def create_listener(conn):
    def inner(path, key, value, is_new):
        return conn.entry_change_callback(key, value, is_new)
    return inner

class TableConn:
    def __init__(self):
        self.table = None
        self.key_commands = {}

    def set_table(self, table):
        self.table = table
        self.table.addEntryListener(create_listener(self))

    def get(self, key, default=None):
        return self.table.getValue(key, default)

    def set(self, key, value):
        self.table.putValue(key, value)

    def add_entry_change_listener(self, func, *keys):
        """
        add a function to be called every time a specific entry is changed on the vision table
        :param func:
        :param keys:
        """
        for key in keys:
            if key not in self.key_commands:
                self.key_commands[key] = []
            self.key_commands[key].append(func)

    def entry_change_callback(self, key, value, is_new):
        """
        runs when an entry is changed on the vision table
        :param key:
        :param value:
        :param is_new:
        """
        if key not in self.key_commands:
            return
        for operation in self.key_commands[key]:
            operation(value)


def net_init(ip=NETWORK_TABLES_IP, table_name=VISION_TABLE_NAME):
    """
    initializes all network values

    """
    vision_conn = TableConn()
    NetworkTables.initialize(ip)
    vision_conn.set_table(NetworkTables.getTable(table_name))

    return vision_conn

# fuck this git
