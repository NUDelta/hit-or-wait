

# assume a user is in the search region
# for each intersection in the search region, we decide whether to ping on the street the person is going or not
# how many steps look ahead? one state?

# finite time horizon: steps required
# how many intersections left in a large search region


# should take into account directionality.
# based on that think about how many steps look ahead


"""
testRoadDict = {('Custer Avenue', 'Hull Terrace'): 0.06249047401310776, ('Custer Avenue', 'Austin Street'): 0.12498094802621552, ('Custer Avenue', 'Mulford Street'): 0.06249047401310776, ('Austin Street', 'Sherman Avenue'): 1.0, ('Custer Avenue', 'Case Street'): 0.03124523700655388}
"""


class itemSearch:
    def __init__(self, intersections):
        self.searchPaths = []
        self.intersections = intersections
        self.itemFoundCount = 0

        self.values = {}
        for i in self.intersections:
            print i
            lookup = {'v': False, 'r': False, 'c': 0, 'l': False}
            self.values[i] = lookup
            # self.intersections[i]['v'] = False # not visited
            # self.intersections[i]['r'] = False # region to search
            # self.intersections[i]['c'] = 0     # search count
            # self.intersections[i]['l'] = False     # item found count
        print self.intersections
        print self.values

    def addSearchRegionDown(self,region):
        self.values[region]['r'] = True

    def expDecay(self, num):
        return (1/2.0) ** num

    def computeWaitingDecisionTable(self, roadPredictModel, maxTime):
        knownValues = []
        knownDecisions = []

        for t in range(0, maxTime):
            knownValues.append({})
            knownDecisions.append({})

        # what should be the nodes? what are the states? intersections!
        # need to show the intersections
        for i in self.intersections:
            print self.values[i]['r']
            if self.values[i]['r']:
                # what is this??
                knownValues[0][i] = self.expDecay(self.values[i]['c'])
                knownDecisions[0][i] = "Hit"
            else:
                knownValues[0][i] = 0
                knownDecisions[0][i] = "Wait"

        for t in range(1, maxTime):
            print str(t) + " steps left\n\n"
            for stateIndex in range(0,len(self.intersections)):
                state = self.intersections[stateIndex]
                print "state is: " + state + " and index is: " + str(stateIndex)

                # base value is if stop right now
                if self.values[state]['r']:
                    knownValues[t][state] = self.expDecay(self.values[state]['c'])
                else:
                    knownValues[t][state] = 0
                knownDecisions[t][state] = "Hit"

                # see if waiting is better
                expectedValue = 0;

                # how many states look ahead? what are the possible options?
                for nextStateIndex in range(stateIndex+1,len(self.intersections)):
                    nextState = self.intersections[nextStateIndex]
                    print "next state is: " + nextState + " and index is: " + str(nextStateIndex)

                    # print "-----printing =========" + str(next)"
                    print "road predict Model: "
                    print roadPredictModel[nextState]
                    print "knownValues: "
                    print knownValues[t-1][nextState]
                    expectedValue += roadPredictModel[nextState] * knownValues[t-1][nextState]
                    print "expected value: "
                    print expectedValue
                if expectedValue > knownValues[t][state]:
                    # decision is to WAIT
                    knownValues[t][state] = expectedValue
                    knownDecisions[t][state] = "Wait"
        return {'values': knownValues, 'decisions': knownDecisions}


    #TODO:
    #call this

    # def requestSearchHitorWait(self, intersection, decisions):
    #     """
    #     INPUT: current intersection
    #     ALG: Hit-or-Wait Decision Theoretic Alg to compute
    #          best decision (to hit or wait) as a person walks
    #          through the region
    #     Hyp: this is the correct decision-theoretic solution
    #     """
    #     maxTime = len(decisions['decisions'])

    #     # TODO: check for off by one
    #     for (index, n) in enumerate(path):
    #         if index >= maxTime:
    #             break

    #         if self.G.node[n]['r'] and decisions['decisions'][maxTime - index - 1][n] == "Hit":
    #             self.G.node[n]['c'] +=1

    #             print "searching for lost item at %s" % (n,)
    #             print ".. at index %s and decision point %s" % (index, maxTime-index)


    #             if self.G.node[n]['l']:
    #                 self.itemFoundCount += 1

    #             break
