from networktables import NetworkTables

from .net_consts import *

# NetworkTables notifier kinds.
NT_NOTIFY_NONE = 0x00
NT_NOTIFY_IMMEDIATE = 0x01  # initial listener addition
NT_NOTIFY_LOCAL = 0x02  # changed locally
NT_NOTIFY_NEW = 0x04  # newly created entry
NT_NOTIFY_DELETE = 0x08  # deleted
NT_NOTIFY_UPDATE = 0x10  # value changed
NT_NOTIFY_FLAGS = 0x20  # flags changed


def fix_func(func):
    return lambda source, key, value, is_new: func(value)


class TableConn:
    def __init__(self, ip=NETWORK_TABLES_IP, table_name=VISION_TABLE_NAME, initialize=True):
        """
            initializes all network values

        """
        if initialize:
            NetworkTables.initialize(ip)
        self.table = NetworkTables.getTable(table_name)
        self.key_commands = {}

    def set_table(self, table):
        self.table = table

    def get(self, key, default=None):
        return self.table.getValue(key, default)

    def set(self, key, value):
        self.table.putValue(key, value)

    def add_entry_change_listener(self, func, key, notify_now=True, notify_local=True):
        """
        add a function to be called every time a specific entry is changed on the vision table
        :param func:
        :param key:
        :param notify_now:
        :param notify_local:
        """
        self.table.addEntryListener(fix_func(func), key=key, localNotify=notify_local, immediateNotify=notify_now)
