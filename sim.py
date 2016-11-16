from itemSearch import HitorWait
from intersection import RoadAPI


# roadapi = RoadAPI()
# predictModelDict = None

# selected some chunks from one runkeeper's running trace and stored data traces as road sequence.
# randomly selected some rows from the one runkeeper user's running trace

# latlngPairs = open('testData.out','r').readlines()
# for i in latlngPairs:
#     tmp = i.split(",")
#     currentLat, currentLng = tmp[0].strip(), tmp[1].split("\r")[0].strip()

#     if roadapi.getRoadIntersection(currentLat,currentLng) != None:
#         currentRoad, intersectionName = roadapi.getRoadIntersection(currentLat,currentLng)
#         predictModelDict = roadapi.getNextRoadProb(currentRoad, intersectionName)

# choosing three intersections as state
intersectionList = ['Custer Avenue+Hull Terrace', 'Custer Avenue+Austin Street', 'Custer Avenue+Mulford Street']
hitorwait = HitorWait(intersectionList)

predictModelDict = {u'Custer Avenue+Hull Terrace': 0.06249047401310776, u'Austin Street+Sherman Avenue': 1.0, u'Custer Avenue+Mulford Street': 0.06249047401310776, u'Custer Avenue+Austin Street': 0.12498094802621552, u'Custer Avenue+Case Street': 0.03124523700655388}

# for k,v in predictModelDict.iteritems():
#     print k,v
hitorwait.addSearchRegionDown('Custer Avenue+Austin Street')
decisions = hitorwait.computeWaitingDecisionTable(predictModelDict, 3)

print decisions

# input: lat,lng pair
# check if the (lat,lng) is in intersectionList
# if it is, run hit or wait algo based on the decision
# update the decision table
# show the decision table



"""
    ##################################################################
    need better job on deciding which intersections for searches

    TODO:
    1) get next road probability
        - take as input all the roads at the intersection
        - show the probability based on previous road sequence

    2) need a boundary for search region
        - currently it's just marking search region
    3) think about what does steps, terminal state mean?
        - can we just use # of intersections in the large search region and use it as steps?
    4) can we improve value of search so that it is more than # of search counts?
    5) should take into account directionality based on that think about how many steps look ahead
        - maybe this point can be resolved when 1) is resolved.
    6)

    ##################################################################

    yk notes:
    # how do you wanna show the state?
    # what is the terminal state?
    #

    # use intersections as state
    # how do you get intersections as state? --> what are the intersections that it has in the lost item region?
    # if a user come across the intersection we pull out the decision table

    # assume a user is in the search region
    # for each intersection in the search region, we decide whether to ping on the street the person is going or not
    # how many steps look ahead? one state?

"""
