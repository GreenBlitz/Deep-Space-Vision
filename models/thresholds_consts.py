from utils import Threshold

# [[19, 45], [88, 191], [112, 203]]
# [[33, 47], [110, 148], [139, 168]]
FUEL_THRESHOLD = Threshold(
    # [[33, 45], [90, 182], [129, 194]],
    [[30, 46], [79, 170], [167, 254]],
    'HLS'
)

# [[34, 91], [11, 73], [9, 126]]
# [[68, 108], [27, 53], [4, 139]]
# [[69, 98], [17, 81], [22, 138]],
TRASH_THRESHOLD = Threshold(
    
    [[52, 102], [88, 142], [36, 76]],
    'HLS'
)


# [[6, 13], [77, 163], [182, 254]],
CARGO_THRESHOLD = Threshold(
    [[1, 30], [55, 168], [174, 255]],
    'HLS'
)

HATCH_PANEL_THRESHOLD = Threshold(
    [[18, 34], [32, 97], [134, 254]],
    'HLS'
)

VISION_TARGET_THRESHOLD = Threshold(
    [[30, 79], [113, 234], [0, 55]],
    'BGR'
)
