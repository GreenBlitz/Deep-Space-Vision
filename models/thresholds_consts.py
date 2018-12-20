from utils import Threshold

# FUEL_THRESHOLD = [[19, 45], [ 88, 191], [112 , 203]]
# FUEL_THRESHOLD = [[33, 47], [110, 148], [139, 168]]
FUEL_THRESHOLD = Threshold(
    [[33, 45], [90, 182], [129, 194]],
    'HLS'
)

# TRASH_THRESHOLD = [[34, 91], [11, 73], [9, 126]]
# TRASH_THRESHOLD = [[68, 108], [27, 53], [4, 139]]
# TRASH_THRESHOLD = [[69, 98], [17, 81], [22, 138]],
TRASH_THRESHOLD = Threshold(
    
    [[52, 102], [88, 142], [36, 76]],
    'HLS'
)
