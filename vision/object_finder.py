
class ObjectFinder:
    def __init__(self, threshold_func, object_descriptor):
        self.threshold = threshold_func
        self.im_object = object_descriptor

    def __call__(self, frame, camera):
        pass  # abstract method (fuck karel this is how you write abstract in python)
