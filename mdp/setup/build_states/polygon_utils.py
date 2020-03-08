
# Algorithm: https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
# TODO: need to understand this algorithm lol
def is_clockwise(polygon):
    result = 0
    for i in range(0, len(polygon)):
        v1 = polygon[i%len(polygon)]
        v2 = polygon[(i+1)%len(polygon)]

        result += (v2[0] - v1[0])*(v2[1]+v1[1])
    return result > 0