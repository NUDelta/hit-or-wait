from shapely.geometry import Point, Polygon
import numpy as np

"""
    To represent gray areas of campus, we will consider a given location's state to be the closest building.
    - To find all adjacent states, we must divide the entire campus into a Voronoi diagram. A Voronoi diagram divides a space
        into regions equidistant from points.
    - But for our case, we are dealing with polygons instead of points. Instead of a Voronoi diagram, we will need a structure called a Medial Axis.
    - ... (more details to follow)

    See Bill's answer for more details: https://stackoverflow.com/questions/36015521/generating-a-voronoi-diagram-around-2d-polygons/36016656
"""

def get_circumcenter(vertex1, vertex2, vertex3):
    bisector1 = find_equation_of_perp(vertex1, vertex2)
    bisector2 = find_equation_of_perp(vertex2, vertex3)
    return find_intersection(bisector1, bisector2)

def find_intersection(eq1, eq2):
    a = [[eq1[0], eq1[1]], [eq2[0], eq2[1]]]
    b = [eq1[2], eq2[2]]
    y, x = np.linalg.solve(a, b)
    return x, y

def midpoint(a1, a2, b1, b2):
    return (a1 + b1) / 2, (a2 + b2) / 2

def find_slope_of_perp(a1, a2, b1, b2):
    if (b2 - a2) == 0:
        return 0
    return (a1 - b1) / (b2 - a2)

# returns equation as a tuple (a, b, c), where a.x + b.y = c
def find_equation_of_perp(vertex1, vertex2):
    a1, a2 = vertex1
    b1, b2 = vertex2
    mid = midpoint(a1, a2, b1, b2)

    slope = find_slope_of_perp(a1, a2, b1, b2)

    if slope == 0 and (b2 - a2) == 0:
        return 0, 1, mid[0]
    else:
        return 1, -slope, mid[1] - slope * mid[0]