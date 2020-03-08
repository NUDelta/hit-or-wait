import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
from shapely.geometry import Polygon, LineString, MultiPoint
from shapely.ops import split
import triangle as tr
from math import *

A = {'vertices': np.array([[0, 0], [0, 1], [1, 1], [1, 0]])}
B = tr.triangulate(A, 'a0.2')
# print(list(map(lambda x: list(map(lambda y: B["vertices"].tolist()[y], x)), B["triangles"].tolist())))

# tr.compare(plt, A, B)
# print(B["vertices"].tolist())
# plt.show()

### Finding circumcenter of triangle

def findIntersectionOfLines(eq1, eq2):
    a = [[eq1[0], eq1[1]], [eq2[0], eq2[1]]]
    b = [eq1[2], eq2[2]]
    y, x = np.linalg.solve(a, b)
    return x, y

def midpoint(a1, a2, b1, b2):
    return ((a1 + b1) / 2, (a2 + b2) / 2)

def findSlopeOfPerpendicularLine(a1, a2, b1, b2):
    if (b2-a2) == 0:
        return 0
    return (a1-b1) / (b2-a2)

# returns equation as a tuple (a, b, c), where a.x + b.y = c
def findEquationOfPerpendicarLine(vertex1, vertex2):
    a1, a2 = vertex1
    b1, b2 = vertex2
    mid = midpoint(a1, a2, b1, b2)

    slope = findSlopeOfPerpendicularLine(a1, a2, b1, b2)

    # account for vertical lines!!
    # TODO: is this wrong?? (account for both horizontal and vertical lines)
    if slope == 0 and (b2-a2) == 0:
        return (0, 1, mid[0])
    else:
        return (1, -slope, mid[1] - slope*mid[0])

def circumcenter(vertex1, vertex2, vertex3):
    bisector1 = findEquationOfPerpendicarLine(vertex1, vertex2)
    bisector2 = findEquationOfPerpendicarLine(vertex2, vertex3)
    return findIntersectionOfLines(bisector1, bisector2)

# print(circumcenter([3.5, 4.5], [6, 6], [0, 6]))


### Find outer polygons
# def findIndexOfMatchingTriangle(side, listOfTriangles):
#     result = []
#     for i in range(0, len(listOfTriangles)):
#         v1, v2 = side
#         if v1 in listOfTriangles[i] and v2 in listOfTriangles[i]:
#             result.append(i)

#         if v1 in listOfTriangles[i] and not v2 in listOfTriangles[i]:
#             result.append(i)

#     return result

def findMatchingTrianglesIndices(vertex, listOfTriangles):
    return [i for i, x in enumerate(listOfTriangles) if vertex in x]

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

def convertTrianglesToLinesWithSmallerAngle(matchingTrianglesIndices, listOfTriangles, vertex):
    result = []
    for i in matchingTrianglesIndices:
        tri = listOfTriangles[i]
        remVertices = list(filter(lambda x: x != vertex, tri))
        
        angles = list(map(lambda x : findAngle(vertex, x), remVertices))
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

def findAllOuterPolygons(listOfInnerPolygons, listOfTriangles, listOfCircumcenters):
    outerPolygons = []
    for innerPoly in listOfInnerPolygons:
        outerPolygons.append(findOuterPolygon(innerPoly, listOfTriangles, listOfCircumcenters))

    return outerPolygons

def findOuterPolygon(innerPoly, listOfTriangles, listOfCircumcenters, plt):
    circumcentersInOuterPoly = []
    count = 0
    for i in range(0, len(innerPoly)):
        plt.text(innerPoly[i][0], innerPoly[i][1], i)

        matchingTrianglesIndices = findMatchingTrianglesIndices(innerPoly[i], listOfTriangles)
        matchingSegments = convertTrianglesToLinesWithSmallerAngle(matchingTrianglesIndices, listOfTriangles, innerPoly[i])
        #append edge of hole to know where to start
        edge = [innerPoly[i], innerPoly[(i-1)%len(innerPoly)]]
        #sort all segments by angle
        matchingSegments.sort(key = lambda x: findAngle(x[0][0], x[0][1]))
        # print(edge)
        # print(matchingSegments)
        # print(list(map(lambda x: listOfTriangles[x[1]], matchingSegments)))
        #find what the starting index (and offset) should be
        offset = 0
        for num in range(0, len(matchingSegments)):
            # print(num)
            # print("here")
            # print(matchingSegments[num][0])
            # print(edge)
            # print(matchingSegments[num][0][0] == edge[0] and matchingSegments[num][0][1] == edge[1] )
            if matchingSegments[num][0][0] == edge[0] and matchingSegments[num][0][1] == edge[1] :
                offset = num
        # print(offset)
        for j in range(0, len(matchingSegments)):
            indexInCircumcenters = matchingSegments[(j+offset)%len(matchingSegments)][1]
            cc = listOfCircumcenters[indexInCircumcenters]
            circumcentersInOuterPoly.append(cc)
            # plt.text(cc[0], cc[1], count)
            # pt = matchingSegments[(j+offset)%len(matchingSegments)][0][1]
            # # print(pt)
            # plt.text(pt[0], pt[1], count)
            count += 1

        circumcentersInOuterPoly.pop()
    # outerPoly = []
    # for i in range(0, len(circumcentersInOuterPoly)):
    #     v1 = circumcentersInOuterPoly[i]
    #     v2 = listOfCircumcenters[triangleIndicesRelatedToOuterPoly[(i+1)%len(triangleIndicesRelatedToOuterPoly)]]
    #     outerPoly += [v1, v2]


    return circumcentersInOuterPoly

### Creating triangulation
def createSegments(*args):
    result = []
    i = 0
    while i < len(args) - 1:
        start = args[i]
        end = args[i+1]
        for j in range(start, end-1):
            result.append([j, j+1])
        result.append([end-1, start])
        i += 1
    return result

def createInterpolatedLine(line, space):
    newLine = []
    for i in range(0, len(line)):
        v1 = line[i]
        v2 = line[(i+1)%len(line)]
        firstRange = np.linspace(v1[0], v2[0], num=space)
        secondRange = np.linspace(v1[1], v2[1], num=space)
        newL = np.dstack((firstRange, secondRange))[0].tolist()
        newL.pop()
        newLine += newL

    return newLine

hole1 = [[-5, -5], [-4, -5], [-4, -4], [-5, -4]]
hole2 = [[3, 3.5], [4, 3], [4.5, 4], [3.5, 4.5]]
hole3 = [[0, 0], [1, 0], [1, 1], [0.5, 1.5], [0, 1]]
bounds = [[-10, -10],  [-10, 10], [10, 10], [10, -10]]

hole1 = createInterpolatedLine(hole1, 5)
hole2 = createInterpolatedLine(hole2, 5)
hole3 = createInterpolatedLine(hole3, 5)
bounds = createInterpolatedLine(bounds, 10)

hole1Centroid = Polygon(hole1).centroid
hole2Centroid = Polygon(hole2).centroid
hole3Centroid = Polygon(hole3).centroid
seg = createSegments(0, len(hole1), len(hole1) + len(hole2), len(hole1) + len(hole2) + len(hole3), len(hole1) + len(hole2) + len(hole3)+ len(bounds))
vertices = np.concatenate((hole1, hole2, hole3, bounds)).tolist()

print(hole3Centroid)

result = tr.triangulate(dict(
    vertices=vertices,
    segments=seg,
    holes=[[hole1Centroid.x, hole1Centroid.y], [hole2Centroid.x, hole2Centroid.y], [hole3Centroid.x, hole3Centroid.y]]
), "p")

tr.compare(plt, {"vertices": np.array(bounds)}, result)
listOfTriangles = []
listOfCircumcenters = []
print(result["triangles"].tolist())
for triangle in result["triangles"].tolist():
    a, b, c = triangle
    print(c)
    x, y = circumcenter(vertices[a], vertices[b], vertices[c])
    listOfTriangles.append([vertices[a], vertices[b], vertices[c]])
    listOfCircumcenters.append([x, y])
    plt.plot(x, y, 'yo')

outerPoly1 = findOuterPolygon(hole1, listOfTriangles, listOfCircumcenters, plt)
poly1 = patches.Polygon(np.array(outerPoly1), color="blue")
plt.gca().add_patch(poly1)

outerPoly2 = findOuterPolygon(hole2, listOfTriangles, listOfCircumcenters, plt)
poly2 = patches.Polygon(np.array(outerPoly2), color="yellow")
plt.gca().add_patch(poly2)

outerPoly3 = findOuterPolygon(hole3, listOfTriangles, listOfCircumcenters, plt)
poly3 = patches.Polygon(np.array(outerPoly3), color="red")
plt.gca().add_patch(poly3)

plt.show()

### Visualizing polygons

# plt.axes()

# poly3 = patches.Polygon(np.array([[0, 0], [0, 6], [6, 6], [6, 0]]), color="yellow")
# plt.gca().add_patch(poly3)

# poly1 = patches.Polygon(np.array([[1, 1], [1, 2], [2, 2], [2, 1]]), color="red")
# plt.gca().add_patch(poly1)

# poly2 = patches.Polygon(np.array([[3, 3.5], [4, 3], [4.5, 4], [3.5, 4.5]]), color="blue")
# plt.gca().add_patch(poly2)

# plt.axis('scaled')
# plt.show()


### Example of using holes
# def circle(N, R):
#     i = np.arange(N)
#     theta = i * 2 * np.pi / N
#     pts = np.stack([np.cos(theta), np.sin(theta)], axis=1) * R
#     seg = np.stack([i, i + 1], axis=1) % N
#     return pts, seg


# pts0, seg0 = circle(30, 1.4)
# pts1, seg1 = circle(16, 0.6)
# pts = np.vstack([pts0, pts1])
# seg = np.vstack([seg0, seg1 + seg0.shape[0]])
# print(seg0)
# print(seg1)
# print(seg)

# A = dict(vertices=pts, segments=seg, holes=[[0, 0]])
# B = tr.triangulate(A, 'qpa0.05')
# tr.compare(plt, A, B)
# plt.show()


### My sample test of triangulation with holes
# hole1 = [[1, 1], [1, 2], [2, 2], [2, 1]]
# hole2 = [[3, 3.5], [4, 3], [4.5, 4], [3.5, 4.5]]
# bounds = [[0, 0], [0, 6], [6, 6], [6, 0]]

# hole1Centroid = Polygon(hole1).centroid
# hole2Centroid = Polygon(hole2).centroid

# print(np.array(bounds))

# result = tr.triangulate(dict(
#     vertices=np.array(bounds + hole1 + hole2),
#     segments=np.array([[2, 2], [2, 4], [4, 4], [4, 2], [2, 2]]),
#     holes=np.array([[3, 3]])
# ), "p")

# tr.compare(plt, {"vertices": np.array(bounds)}, result)
# plt.show()


# print(circumcenter((8, 2), (8, 8), (4, 6)))
