import cv2


class ThresholdGroup:
    def __init__(self, *thresholds):
        self.thresholds = list(thresholds)

    def __call__(self, frame):
        return reduce(lambda th_frame, threshold: cv2.bitwise_or(th_frame, threshold(frame)), self.thresholds)

    def __add__(self, other):
        if isinstance(other, ThresholdGroup):
            return ThresholdGroup(self.thresholds + other.thresholds)
        return ThresholdGroup(self.thresholds + [other])

    def __iter__(self):
        return iter(self.thresholds)

    def __len__(self):
        return len(self.thresholds)

    def __getitem__(self, item):
        return self.thresholds[item]

    def __setitem__(self, key, value):
        self.thresholds[key] = value

    def __iadd__(self, other):
        if isinstance(other, ThresholdGroup):
            self.thresholds += other.thresholds
        else:
            self.thresholds += [other]
        return self
