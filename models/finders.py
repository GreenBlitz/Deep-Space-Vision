from vision import *
from .pipeline_consts import *
from .image_objects_consts import *

# standard objects

find_fuels = CircleFinder(threshold_fuel, FUEL)

find_trash = RectFinder(threshold_trash, TRASH)

find_cargo = CircleFinder(threshold_cargo, CARGO)

find_hatch_panel = CircleFinder(threshold_hatch_panel, HATCH_PANEL)

find_vision_target = RotatedRectFinder(threshold_vision_target, VISION_TARGET)

# non standard object

find_hatch = HatchFinder(threshold_vision_target, VISION_TARGET)

find_port = HatchFinder(threshold_vision_target, VISION_TARGET)