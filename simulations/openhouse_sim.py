#! /usr/bin/env python
from openhouse_lattice import latticeSearch


# Hit-or-wait
def runHitOrWait():
    ex.printLostItem()
    maxTime = 5
    decisions = {}
    for (user, path) in ex.searchPaths:
        decisions[user] = ex.computeWaitingDecisionTable(moveModel[(0,0)], user, maxTime)

    for path in ex.searchPaths:
        ex.requestSearchHitorWait(path, decisions)
        decisions = {}
        for (user, path) in ex.searchPaths:
            decisions[user] = ex.computeWaitingDecisionTable(moveModel[(0,0)], user, maxTime)

    ex.printSearchProgress()
    ex.clearDeliveryRegions()


# Setup 
ex = latticeSearch(3, 3)    # create a lattice for searching
ex.users.addUser("Alice")
ex.users.addUser("Bob")
ex.users.addUser("Morty")
# simulate people walking through
ex.addSearcherPath("Morty", [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)])
# create movement model
pathsForModel = ex.createPaths((0,0), (2,2), 1000)
moveModel = ex.buildMovementModel(pathsForModel)

print("\nMorty's Path:")
print("\U00002193" + "\t" + "-" + "\t" + "-" + "\n")
print("\U00002193" + "\t" + "-" + "\t" + "-" + "\n")
print("\U00002192" + "\t" + "\U00002192" + "\t" + "\U00002192" + "\n")

# First Simulation
print("-------------------------------------")
input("What happens on the first day?\n")
ex.addDeliveryRegion("Alice", 1, 0)
ex.addDeliveryRegion("Bob", 2, 0)
runHitOrWait()

# Second Simulation
print("-------------------------------------")
input("What happens on the second day?\n")
ex.addDeliveryRegion("Alice", 2, 2)
ex.addDeliveryRegion("Bob", 1, 0)
runHitOrWait()

# Second Simulation
print("-------------------------------------")
input("What happens on the third day?\n")
ex.addDeliveryRegion("Alice", 2, 0)
ex.addDeliveryRegion("Bob", 0, 0)
runHitOrWait()


exit()


