#! /usr/bin/env python
from lattice import latticeSearch, users

ex = latticeSearch(10, 10, 20)    # create a lattice for searching
for index, user in enumerate(list(ex.users.G.nodes())[:10]):
    ex.addDeliveryRegion(user, index, index)

#ex.addSearchRegionDown(9)
#ex.addSearchRegionDown(3)
ex.printLostItem()

# simulate people walking through
numSearchers = 10
ex.addSearcherPathsRandom(numSearchers, list(ex.users.G.nodes())[10:20], (0,0), (9,9))  

#    ex.addSearcherPath((9,2), (0,0))  
    # ex.printSearcherPath(i)
ex.printAllPathCount()

#------------------------------ run algs

# ALG: OPTIMAL single step, non-forward looking
#      assume know where people will go, send it to them where count is lowest

for path in ex.searchPaths:
    ex.requestSearchSingleOPT(path)
print("OPTIMAL single step, non-forward looking")
print("Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum)))
ex.printSearchProgress()
ex.clearSearchProgress()



# ALG: greedy first encounter 
#      (go for first cell in search region, regardless of count)
# Hyp: too greedy, will rack up the search count in a lot of places that don't need #      it. 

for path in ex.searchPaths:
    ex.requestSearchFirstAvailable(path)

print("Greedy search at first encounter")
print("Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum)))
ex.printSearchProgress()
ex.clearSearchProgress()


print("-----------------------------")
# for path in ex.searchPaths:
#     ex.requestSearchFirstHitBelowMedianCount(path)
# ex.printSearchProgress()

# create movement model
pathsForModel = ex.createPaths((0,0), (9,2), 1000)
moveModel = ex.buildMovementModel(pathsForModel)

## TODO: this number needs to be set right for the person to know to stop at the end --- maybe this is a thing about the model... that we need the transition model to end at the end or for the world to be defined a little bigger (or to some terminal state).

maxTime = 20
decisions = {}
for (user, path) in ex.searchPaths:
    decisions[user] = ex.computeWaitingDecisionTable(moveModel[(0,0)], user, maxTime)

# print "hello"
# print pathsForModel

# t = 6
# for y in range(0, 10):
#     loc = (y,2)
#     if decisions['decisions'][t][loc] == "Wait":
#         print "with %s steps left, at %s:" % (t, loc)
#         print decisions['decisions'][t][loc]
#         print decisions['values'][t][loc]
#         print moveModel[(0,2)][loc]
#         print "\n"


for path in ex.searchPaths:
    ex.requestSearchHitorWait(path, decisions)
    decisions = {}
    for (user, path) in ex.searchPaths:
        decisions[user] = ex.computeWaitingDecisionTable(moveModel[(0,0)], user, maxTime)

print("Number of Searches: {}, Search Value: {}".format(ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum)))
ex.printSearchProgress()

# print(users().G.edges(data=True))

# #print decisions['decisions'][0]

# ## HQ: need to test more, but wow, can't believe this works!!!
# for y in range(0, 10):
#     loc = (y,2)
#     for i in range(maxTime):
#         if(decisions['decisions'][i][loc] == "Wait"):
#             print "with %s steps left, at %s:" % (i, loc)
#             print decisions['decisions'][i][loc]
#             print decisions['values'][i][loc]
#             print moveModel[(0,0)][loc]
#             print "\n"

# exit()


