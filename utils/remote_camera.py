from .net.table_conn import TableConn
from .net.net_consts import NETWORK_TABLES_IP


class RemoteCamera:
    def __init__(self, cam_index, stream_server, network_table_ip=NETWORK_TABLES_IP):
        self.server = stream_server
        self.table = TableConn(ip=network_table_ip, table_name='camera-%d' % cam_index)
        self.keys_loaded = {}
        self.add_key_waiter('ret_set_exposure')
        self.add_key_waiter('ret_toggle_auto_exposure')
        self.add_key_waiter('ret_get')
        self.add_key_waiter('ret_set')

    def add_key_waiter(self, key):
        self.table.add_entry_change_listener(lambda tmp: self.set_key_loaded(key, True), key)
        self.keys_loaded[key] = False

    def set_key_loaded(self, key, value):
        self.keys_loaded[key] = value

    def wait_key_change(self, key):
        while not self.keys_loaded[key]:
            pass
        return self.table.get(key)

    def read(self):
        frame = self.server.get_frame()
        return frame is not None, frame

    def release(self):
        self.table.set('release', True)
        self.server = None

    def get(self, arg):
        self.set_key_loaded('ret_get', False)
        self.table.set('get', arg)
        return self.wait_key_change('ret_get')

    def set(self, prop_id, value):
        self.set_key_loaded('ret_set', False)
        self.table.set('set_prop_id', prop_id)
        self.table.set('set', value)
        return self.wait_key_change('ret_set')

    def set_exposure(self, exposure):
        self.set_key_loaded('ret_set_exposure', False)
        self.table.set('set_exposure', exposure)
        return self.wait_key_change('ret_set_exposure')

    def toggle_auto_exposure(self, auto):
        self.set_key_loaded('ret_toggle_auto_exposure', False)
        self.table.set('toggle_auto_exposure', auto)
        return self.wait_key_change('ret_toggle_auto_exposure')

    @property
    def view_range(self):
        return self.table.get('view_range')

    @property
    def constant(self):
        return self.table.get('constant')

    @property
    def port(self):
        return self.table.get('port')

    @property
    def width(self):
        return self.table.get('width')

    @property
    def height(self):
        return self.table.get('height')

    def resize(self, x_factor, y_factor):
        self.table.set('resize_x', x_factor)
        self.table.set('resize_y', y_factor)

    def set_frame_size(self, width, height):
        self.table.set('set_frame_width', width)
        self.table.set('set_frame_height', height)

    def toggle_stream(self, should_stream):
        self.table.set('toggle_stream', should_stream)
