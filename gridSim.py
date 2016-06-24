#! /usr/bin/env python
from lattice import latticeSearch

ex = latticeSearch(10, 10)    # create a lattice for searching
ex.addSearchRegionDown(2)     # mark region where item may have been lost
#ex.addSearchRegionDown(9)
#ex.addSearchRegionDown(3)
ex.markLostItem(3,2)          # mark location of lost item
ex.printLostItem()

# simulate people walking through
numSearchers = 30
for i in range(numSearchers):
    ex.addSearcherPath((0,0), (9,2))  
#    ex.addSearcherPath((9,2), (0,0))  
    # ex.printSearcherPath(i)
ex.printAllPathCount()



#------------------------------ run algs

# ALG: OPTIMAL single step, non-forward looking
#      assume know where people will go, send it to them where count is lowest
for path in ex.searchPaths:
    ex.requestSearchSingleOPT(path)
print "OPTIMAL single step, non-forward looking"
print "Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum))
ex.printSearchProgress()
ex.clearSearchProgress()



# ALG: greedy first encounter 
#      (go for first cell in search region, regardless of count)
# Hyp: too greedy, will rack up the search count in a lot of places that don't need #      it. 
for path in ex.searchPaths:
    ex.requestSearchFirstAvailable(path)

print "Greedy search at first encounter"
print "Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum))
ex.printSearchProgress()
ex.clearSearchProgress()


# ALG: node counting greedy (go for first cell with lowest count)
# Hyp: search for lowest but will have few actual searchs, lots of walking by
#      waiting for that best opportunity which never comes
for path in ex.searchPaths:
    ex.requestSearchFirstHitLowestCount(path)

print "Node counting greedy"
print "Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum))
ex.printSearchProgress()
ex.clearSearchProgress()


# ALG: node counting favor lows (below median)
# Hyp: search for low, hit on more searchers, but still good amount of walking by
#      waiting may never come, but not wasting searchers where it's high count and 
#      low value, either.
for path in ex.searchPaths:
    ex.requestSearchFirstHitBelowMedianCount(path)

print "Node counting below median"
print "Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum))
ex.printSearchProgress()
ex.clearSearchProgress()



print "-----------------------------"
# for path in ex.searchPaths:
#     ex.requestSearchFirstHitBelowMedianCount(path)
# ex.printSearchProgress()

# create movement model
pathsForModel = ex.createPaths((0,0), (9,2), 1000)
moveModel = ex.buildMovementModel(pathsForModel)

## TODO: this number needs to be set right for the person to know to stop at the end --- maybe this is a thing about the model... that we need the transition model to end at the end or for the world to be defined a little bigger (or to some terminal state).

maxTime = 12
decisions = ex.computeWaitingDecisionTable(moveModel[(0,0)], maxTime)

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
    decisions = ex.computeWaitingDecisionTable(moveModel[(0,0)], maxTime)

print "Number of Searches: %s, Search Value: %s" % (ex.getTotalSearchCount(), ex.computeSearchValue(ex.expDecaySum))
ex.printSearchProgress()



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

exit()


