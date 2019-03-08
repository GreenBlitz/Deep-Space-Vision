from .stream_camera import StreamCamera, Camera, cv2
from .net.table_conn import TableConn
from .net.net_consts import NETWORK_TABLES_IP


class BroadcastCamera(StreamCamera):
    def __init__(self, port, data, stream_client, cam_index=None, network_table_ip=NETWORK_TABLES_IP,
                 should_stream=False):
        StreamCamera.__init__(self, port, data, stream_client, should_stream)
        if cam_index is None:
            cam_index = port
        self.cam_index = cam_index
        self.table = TableConn(ip=network_table_ip, table_name='camera-%d' % cam_index)
        self.table.add_entry_change_listener(self.remote_set_exposure, 'set_exposure')
        self.table.add_entry_change_listener(self.remote_toggle_auto_exposure, 'toggle_auto_exposure')
        self.table.add_entry_change_listener(lambda tmp: self.release(), 'release')
        self.table.add_entry_change_listener(self.remote_get, 'get')
        self.table.add_entry_change_listener(self.remote_set, 'set')
        self.table.add_entry_change_listener(self.remote_resize_x, 'resize_x')
        self.table.add_entry_change_listener(self.remote_resize_y, 'resize_y')
        self.table.add_entry_change_listener(self.remote_set_frame_width, 'set_frame_width')
        self.table.add_entry_change_listener(self.remote_set_frame_height, 'set_frame_height')
        self.table.add_entry_change_listener(self.toggle_stream, 'toggle_stream')

        self.remote_sync()

    def remote_set_exposure(self, value):
        ret = self.set_exposure(value)
        self.table.set('ret_set_exposure', ret)

    def remote_toggle_auto_exposure(self, value):
        ret = self.toggle_auto_exposure(value)
        self.table.set('ret_toggle_auto_exposure', ret)

    def remote_get(self, value):
        ret = self.get(value)
        self.table.set('ret_get', ret)

    def remote_set(self, value):
        ret = self.set(self.table.get('set_prop_id'), value)
        self.table.set('ret_set', ret)

    def remote_resize_x(self, f_x):
        self.stream_server.fx *= f_x
        self.resize(f_x, 1)
        self.remote_sync()

    def remote_resize_y(self, f_y):
        self.stream_server.fy *= f_y
        self.resize(1, f_y)
        self.remote_sync()

    def remote_set_frame_width(self, width):
        self.stream_server.fx = width / Camera.get(self, cv2.CAP_PROP_FRAME_WIDTH)
        self.set_frame_size(width, self.height)
        self.remote_sync()

    def remote_set_frame_height(self, height):
        self.stream_server.fy = height / Camera.get(self, cv2.CAP_PROP_FRAME_HEIGHT)
        self.resize(self.width, height)
        self.remote_sync()

    def remote_sync(self):
        self.table.set('width', self.width)
        self.table.set('height', self.height)
        self.table.set('view_range', self.view_range)
        self.table.set('constant', self.constant)
        self.table.set('port', self.port)
