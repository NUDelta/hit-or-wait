import json
from build_states import create_evanston_polygons, create_medial_axis_as_outer_polygons
import os

print(os.path.dirname("buildings.json"))

with open("buildings.json") as data:
    buildings = json.load(data)

evanston_polygons = create_evanston_polygons(buildings)

left_top = [42.063650, -87.692412]
right_top = [42.063650, -87.667343]
right_bottom = [42.040201, -87.667343]
left_bottom = [42.040201, -87.692412]

bounds = [left_top, left_bottom, right_bottom, right_top]

outer_polygons = create_medial_axis_as_outer_polygons(evanston_polygons[17:20], bounds)
