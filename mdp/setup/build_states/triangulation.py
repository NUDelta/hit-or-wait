from shapely.geometry import Polygon, Point
import numpy as np
import triangle as tr
import matplotlib.pyplot as plt
from matplotlib import patches
import random
from .polygon_utils import is_clockwise

### Creating triangulation
def polygons_to_triangulation(polygons, bounds):

    # TODO: create_interpolated_poly(...)
    polygons = [create_interpolated_poly(convert_to_list_of_points(poly), 2) for poly in polygons]
    bounds = create_interpolated_poly(bounds, 10)

    # polygons = [[[(pt[0] - 42)*1000, (pt[1] - 87.6)* 1000] for pt in poly] for poly in polygons]
    # bounds = [[(pt[0] - 42)*1000, (pt[1] - 87.6) * 1000] for pt in bounds]

    polygons_plus_bounds = polygons + [bounds]
    segments = create_segments(polygons_plus_bounds)
    holes = create_holes(polygons)
    vertices = create_vertices(polygons_plus_bounds)
    result = tr.triangulate(dict(
        vertices=vertices,
        segments=segments,
        holes=holes,
    ), "p")
    return (result, polygons, vertices)

def create_segments(polygons):
    result = []

    temp = 0
    pointers = [0]
    for poly in polygons:
        pointers.append(len(poly) + temp)
        temp += len(poly)

    for i in range(0, len(pointers) - 1) :
        start = pointers[i]
        end = pointers[i+1]
        for j in range(start, end-1):
            result.append([j, j+1])
        result.append([end-1, start])
    return result

def create_holes(polygons):
    return [get_random_point_in_polygon(poly) for poly in polygons]

def create_vertices(polygons):
    return np.concatenate(polygons).tolist()

def convert_to_list_of_points(polygon):
    polygon = list(polygon["polygon"].exterior.coords)
    if is_clockwise(polygon):
        print("here")
        polygon.reverse()
    return list(map(lambda x: [x[0], x[1]], polygon[:-1]))

def get_random_point_in_polygon(polygon):
    polygon = Polygon(polygon)
    minx, miny, maxx, maxy = polygon.bounds
    while True:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(pnt):
            return [pnt.x, pnt.y]

def create_interpolated_poly(poly, space):
    newLine = []
    for i in range(0, len(poly)):
        v1 = poly[i]
        v2 = poly[(i+1)%len(poly)]
        firstRange = np.linspace(v1[0], v2[0], num=space)
        secondRange = np.linspace(v1[1], v2[1], num=space)
        newL = np.dstack((firstRange, secondRange))[0].tolist()
        newL.pop()
        newLine += newL

    return newLine