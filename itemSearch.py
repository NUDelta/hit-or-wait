class HitorWait:
    def __init__(self, intersections):
        self.searchPaths = []
        self.intersections = intersections
        self.itemFoundCount = 0
        self.values = {}

        for i in self.intersections:
            print i
            lookup = {'v': False, 'r': False, 'c': 0, 'l': False}
            # 'v' not visited, 'r' region to search, 'c' search count, 'l', lost item found
            self.values[i] = lookup

        # print self.intersections
        # print self.values

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

        for i in self.intersections:
            if self.values[i]['r']:
                # what is this??
                knownValues[0][i] = self.expDecay(self.values[i]['c'])
                knownDecisions[0][i] = "Hit"
            else:
                knownValues[0][i] = 0
                knownDecisions[0][i] = "Wait"

        for t in range(1, maxTime):
            for stateIndex in range(0,len(self.intersections)):
                state = self.intersections[stateIndex]

                """
                 need to work on what it means to be 'search region' in our scenario
                 b/c we only make decisions when people are in the 'search region'
                 if it is something like a road/region needs attention, how do we prioritize and mark these roads or regions?
                """

                # based value is 1 if it is marked as search region, otherwise 0.
                if self.values[state]['r']:
                    knownValues[t][state] = self.expDecay(self.values[state]['c'])
                else:
                    knownValues[t][state] = 0

                # base decision is always hit
                knownDecisions[t][state] = "Hit"

                # see if waiting is better
                expectedValue = 0;

                """
                how many states (in current implementation, how many intersections) to look ahead?
                what are the possible options?
                """
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
