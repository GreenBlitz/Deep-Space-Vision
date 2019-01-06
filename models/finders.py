from vision import *
from pipeline_consts import *
from image_objects_consts import *

find_fuels = CircleFinder(threshold_fuel, FUEL)

find_trash = RectFinder(threshold_trash, TRASH)

find_cargo = CircleFinder(threshold_cargo, CARGO)

find_hatch_panel = CircleFinder(threshold_hatch_panel, HATCH_PANEL)
