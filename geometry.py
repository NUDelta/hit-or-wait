import json
from shapely.geometry import Point, Polygon
import sys

poly = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
print(poly.contains(Point(0.9, 0.3)))
print(poly.contains(Point(-1, 0.3)))
print(poly.distance(Point(0, 3)))

with open("buildings.json") as data:
    buildingsJson = json.load(data)

def createPolygonObjectFromBuilding(building):
    result = {}
    result["name"] = building["name"]
    result["polygon"] = createPolygonFromPoints(building["points"])
    return result

def convertLocationToTuple(loc):
    return Point(loc["lat"], loc["lng"])

def createPolygonFromPoints(points):
    return Polygon(list(map(convertLocationToTuple, points)))

polygons = list(map(createPolygonObjectFromBuilding, buildingsJson))

mudd = Point(42.058283, -87.674422)
polyFound = 0

for poly in polygons:
    if poly["polygon"].contains(mudd):
        polyFound = poly

assert(polyFound != 0 and "Mudd" in polyFound["name"])

nearTech = Point(42.052130, -87.689330)
polyFound = 0
closestPoly = 0
tempDist = sys.maxsize

for poly in polygons:
    if poly["polygon"].contains(nearTech):
        polyFound = poly
    else:
        currDist = poly["polygon"].distance(nearTech)
        if currDist < tempDist:
            tempDist = currDist
            closestPoly = poly

print(polyFound)
print(closestPoly)

# finding adjacent buildings
# - dividing imto voronoi diagram of polygons (finding medial axis)

