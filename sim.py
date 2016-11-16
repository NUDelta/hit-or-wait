"""
testRoadDict = {('Custer Avenue', 'Hull Terrace'): 0.06249047401310776, ('Custer Avenue', 'Austin Street'): 0.12498094802621552, ('Custer Avenue', 'Mulford Street'): 0.06249047401310776, ('Austin Street', 'Sherman Avenue'): 1.0, ('Custer Avenue', 'Case Street'): 0.03124523700655388}
"""
from itemSearch import itemSearch
import intersection as its

ex = itemSearch(['Custer Avenue+Hull Terrace', 'Custer Avenue+Austin Street', 'Custer Avenue+Mulford Street'])

predictModelDict = {'Custer Avenue+Hull Terrace': 0.06249047401310776, 'Custer Avenue+Austin Street': 0.12498094802621552, 'Custer Avenue+Mulford Street': 0.06249047401310776, 'Austin Street+Sherman Avenue': 1.0, 'Custer Avenue+Case Street': 0.03124523700655388}

print predictModelDict
ex.addSearchRegionDown('Custer Avenue+Austin Street')
decisions = ex.computeWaitingDecisionTable(predictModelDict, 3)

print decisions

its.loadPreviousHistory
# its.getRoadIntersection(42.022407, -87.680435)

latlngPairs = open('testData.out','r').readlines()
for i in latlngPairs:
    tmp = i.split(",")
    currentLat, currentLng = tmp[0].strip(), tmp[1].split("\r")[0].strip()
    # print currentLat, currentLng
    its.getRoadIntersection(currentLat,currentLng)
