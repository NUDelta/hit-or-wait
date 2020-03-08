from .triangulation import polygons_to_triangulation
import triangle as tr
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
from math import *
from .triangle_utils import get_circumcenter
import random

def create_medial_axis_as_outer_polygons(polygons, bounds):
    triangulations, new_polys, vertices = polygons_to_triangulation(polygons[0:20], bounds)
    tr.compare(plt, {"vertices": np.array(bounds)}, triangulations)
    listOfTrianglesAndCircumcenters = []
    for triangle in triangulations["triangles"].tolist():
        a, b, c = triangle
        x, y = get_circumcenter(vertices[a], vertices[b], vertices[c])
        listOfTrianglesAndCircumcenters.append({
            "circumcenter": [x, y],
            "triangle": [vertices[a], vertices[b], vertices[c]]
        })
        # plt.plot(x, y, 'yo')

    for poly in new_polys:
        outerPoly = findOuterPolygon(poly, listOfTrianglesAndCircumcenters, plt)
        print("ANSWER")
        print(len(outerPoly))
        # for i in range(0, len(outerPoly)):
        #     plt.text(outerPoly[i][0], outerPoly[i][1], i)
        # print(outerPoly)
        patch = patches.Polygon(np.array(outerPoly), color=(random.random(), random.random(), random.random()))
        # print(outerPoly)
        # for i in range(0, len(outerPoly)):
        #     # plt.text(outerPoly[i][0], outerPoly[i][1], i)
        #     pass
        plt.gca().add_patch(patch)
    plt.show()

# for triangle in result["triangles"].tolist():
#     a, b, c = triangle
#     print(c)
#     x, y = circumcenter(vertices[a], vertices[b], vertices[c])
#     listOfTriangles.append([vertices[a], vertices[b], vertices[c]])
#     listOfCircumcenters.append([x, y])
#     plt.plot(x, y, 'yo')
#
# outerPoly1 = findOuterPolygon(hole1, listOfTriangles, listOfCircumcenters, plt)
# poly1 = patches.Polygon(np.array(outerPoly1), color="blue")
# plt.gca().add_patch(poly1)
#
# outerPoly2 = findOuterPolygon(hole2, listOfTriangles, listOfCircumcenters, plt)
# poly2 = patches.Polygon(np.array(outerPoly2), color="yellow")
# plt.gca().add_patch(poly2)
#
# outerPoly3 = findOuterPolygon(hole3, listOfTriangles, listOfCircumcenters, plt)
# poly3 = patches.Polygon(np.array(outerPoly3), color="red")
# plt.gca().add_patch(poly3)s


### Find outer polygons
def findMatchingTrianglesIndices(vertex, listOfTrianglesAndCircumcenters):
    return [i for i, x in enumerate(listOfTrianglesAndCircumcenters) if vertex in x["triangle"]]

# def findAngle(v1, v2):
#     angle = np.rad2deg(np.arctan2(v2[1] - v1[1], v2[0] - v1[0]))
#     return angle

def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return a

def findAngle(v1, v2):
    x_orig, y_orig = v1
    x_landmark, y_landmark = v2
    deltaY = y_landmark - y_orig
    deltaX = x_landmark - x_orig
    return np.rad2deg(angle_trunc(atan2(deltaY, deltaX)))

def convertTrianglesToLinesWithSmallerAngle(matchingTrianglesIndices, listOfTrianglesAndCircumcenters, vertex):
    result = []
    for i in matchingTrianglesIndices:
        tri = listOfTrianglesAndCircumcenters[i]["triangle"]
        remVertices = list(filter(lambda x: x != vertex, tri))

        angles = list(map(lambda x: findAngle(vertex, x), remVertices))
        # it's messy because we need to get the smaller angle, looking counter-clockwise, but, for example, 355 > 10
        if angles[0] > angles[1]:
            larger = 0
            smaller = 1
        else:
            larger = 1
            smaller = 0
        isMessy = (angles[larger] - angles[smaller]) > 180
        if isMessy:
            result.append(([vertex, remVertices[larger]], i))
        else:
            result.append(([vertex, remVertices[smaller]], i))
    return result


def findAllOuterPolygons(listOfInnerPolygons, listOfTriangles, listOfCircumcenters, plt):
    outerPolygons = []
    for innerPoly in listOfInnerPolygons:
        outerPolygons.append(findOuterPolygon(innerPoly, listOfTriangles, listOfCircumcenters, plt))

    return outerPolygons

def findOuterPolygon(innerPoly, listOfTrianglesAndCircumcenters, plt):

    circumcentersAndTrianglesInOuterPoly = []
    count = 0
    print(len(listOfTrianglesAndCircumcenters))
    # REMOVE ALL TRIANGLES WITH VERTICES ONLY IN INNER POLYGON
    temp = list(filter(lambda x: not x["triangle"][0] in innerPoly or not x["triangle"][1] in innerPoly or not x["triangle"][2] in innerPoly, listOfTrianglesAndCircumcenters))
    listOfTrianglesAndCircumcenters = temp
    print(len(listOfTrianglesAndCircumcenters))

    for i in range(0, len(innerPoly)):
        # plt.text(innerPoly[i][0], innerPoly[i][1], i)

        matchingTrianglesIndices = findMatchingTrianglesIndices(innerPoly[i], listOfTrianglesAndCircumcenters)

        # print("poly")
        # print(innerPoly)
        # print("tri")

        # REMOVE ALL TRIANGLES WITH VERTICES ONLY IN INNER POLYGON
        # print(len(matchingTrianglesIndices))
        # matchingTrianglesIndices = list(
        #     filter(lambda x: not listOfTriangles[x][0] in innerPoly or not listOfTriangles[x][1] in innerPoly or not listOfTriangles[x][2] in innerPoly, matchingTrianglesIndices))
        # print(len(matchingTrianglesIndices))
        matchingSegments = convertTrianglesToLinesWithSmallerAngle(matchingTrianglesIndices, listOfTrianglesAndCircumcenters,
                                                                   innerPoly[i])
        # append edge of hole to know where to start
        # SOMETIMES, in concave cases, direct vertex before is not first one
        foundEdge = False
        lookBack = 1
        while not foundEdge and lookBack < len(innerPoly):
            edge = [innerPoly[i], innerPoly[(i - lookBack) % len(innerPoly)]]
            # sort all segments by angle
            matchingSegments.sort(key=lambda x: findAngle(x[0][0], x[0][1]))
            # print(edge)
            # print(matchingSegments)
            # print(list(map(lambda x: listOfTriangles[x[1]], matchingSegments)))
            # find what the starting index (and offset) should be
            offset = 0
            for num in range(0, len(matchingSegments)):
                # print(num)
                # print("here")
                # print(matchingSegments[num][0])
                # print(edge)
                # print(matchingSegments[num][0][0] == edge[0] and matchingSegments[num][0][1] == edge[1])


                if matchingSegments[num][0][0] == edge[0] and matchingSegments[num][0][1] == edge[1]:
                    offset = num
                    foundEdge = True
                    break
            # if not foundEdge:
            #     plt.show()
            lookBack += 1


        # print(offset)
        for j in range(0, len(matchingSegments)):
            indexInCircumcenters = matchingSegments[(j + offset) % len(matchingSegments)][1]
            cc = listOfTrianglesAndCircumcenters[indexInCircumcenters]["circumcenter"]
            circumcentersAndTrianglesInOuterPoly.append(listOfTrianglesAndCircumcenters[indexInCircumcenters])

            # plt.text(cc[0], cc[1], count)
            pt = matchingSegments[(j+offset)%len(matchingSegments)][0][1]
            # print(pt)
            # plt.text(pt[0], pt[1], count)

            count += 1
        if len(circumcentersAndTrianglesInOuterPoly) > 0 and twoVerticesInTriangle(circumcentersAndTrianglesInOuterPoly[-1]["triangle"], innerPoly):
            circumcentersAndTrianglesInOuterPoly.pop()

    return list(map(lambda x: x["circumcenter"], circumcentersAndTrianglesInOuterPoly))

def twoVerticesInTriangle(tri, poly):
    verticesInTri = list(filter(lambda x: x in poly, tri))
    return len(verticesInTri) > 1

# have an edge to [building_id] representation

# polygons_to_triangulation(evanston_polygons[0:20], bounds)
# tr.compare(plt, {"vertices": np.array(bounds)}, result)
#  plt.show()

# evanston_polygons[0:10] + evanston_polygons[25:32] + evanston_polygons[40:50] + evanston_polygons[60:180] + evanston_polygons[200:210]


