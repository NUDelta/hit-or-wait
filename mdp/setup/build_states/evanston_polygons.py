from shapely.geometry import Polygon, Point
"""
    Convert campus buildings to polygons
"""

def create_evanston_polygons(buildings):
    campus_polygons = list(map(create_polygon, buildings))
    return filter_in_evanston(campus_polygons)

def create_polygon(building):
    result = {}
    result["name"] = building["name"]
    result["polygon"] = convert_points_to_polygon(building["points"])
    return result

def convert_points_to_polygon(points):
    return Polygon(list(map(create_tuple, points)))

def create_tuple(loc):
    return Point(loc["lat"], loc["lng"])

def filter_in_evanston(polygons):
    left_top = [42.063650, -87.692412]
    right_top = [42.063650, -87.667343]
    right_bottom = [42.040201, -87.667343]
    left_bottom = [42.040201, -87.692412]

    boundary = Polygon([left_top, left_bottom, right_bottom, right_top])

    evanstonBuildings = list(
        filter(lambda x: boundary.contains(x["polygon"]), polygons)
    )

    return evanstonBuildings