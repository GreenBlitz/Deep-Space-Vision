class CameraData:
    def __init__(self, surface_constant, fov):
        self.constant = surface_constant
        self.view_range = fov

    def __cmp__(self, other):
        return self.constant == other.constant and self.view_range == other.view_range
