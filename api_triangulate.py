import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np
from shapely.geometry import Polygon
import triangle as tr

A = {'vertices': np.array([[0, 0], [0, 1], [1, 1], [1, 0]])}
B = tr.triangulate(A, 'a0.2')
# print(list(map(lambda x: list(map(lambda y: B["vertices"].tolist()[y], x)), B["triangles"].tolist())))

# tr.compare(plt, A, B)
# print(B["vertices"].tolist())
# plt.show()


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
    print(result)
    return result

hole1 = [[1, 1], [2, 1], [2, 2], [1, 2]]
hole2 = [[3, 3.5], [3.5, 4.5], [4.5, 4], [4, 3]]
bounds = [[0, 0], [0, 6], [6, 6], [6, 0]]

hole1Centroid = Polygon(hole1).centroid
hole2Centroid = Polygon(hole2).centroid
seg = createSegments(0, len(hole1), len(hole1) + len(hole2), len(hole1) + len(hole2) + len(bounds))
print(seg)
result = tr.triangulate(dict(
    vertices=bounds + hole1 + hole2,
    segments=seg,
    holes=[[hole1Centroid.x, hole1Centroid.y], [hole2Centroid.x, hole2Centroid.y]]
), "p")

tr.compare(plt, {"vertices": np.array(bounds)}, result)
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
