import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import numpy
import collections

class latticeSearch:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.G=nx.grid_2d_graph(h, w)
        self.searchPaths = []
        self.itemFoundCount = 0

        for x in range(0, h):
            for y in range(0, w):
                self.G.node[(x,y)]['v'] = False  # not visited
                self.G.node[(x,y)]['r'] = False  # region to search
                self.G.node[(x,y)]['c'] = 0      # search count
                self.G.node[(x,y)]['l'] = False

################# MODEL MOVEMENT ###########################
    def addSearcherPath(self, start, end):
        path = random.choice(list(nx.all_shortest_paths(self.G, start, end)))
        self.searchPaths.append(path)
        return path

    def createPaths(self, start, end, numPaths):
        paths = []
        for p in range(numPaths):
            path = random.choice(list(nx.all_shortest_paths(self.G, start, end)))
            paths.append(path)
        # print "=====path====="
        # print path
        return paths


    def buildMovementModel(self, paths):
        """
           Based on a set of paths, build a model of
               Prob(nextLocation | startLocation, currentLocation)
           Returns: Dict[startLocation][currentLocation] = P(nextLcation)
           Assumes: When no paths through s in data, assume P(s->s') = 1 / len(s')
        """

        startDict = {}
        for p in paths:
            if p[0] in startDict:
                startDict[p[0]].append(p)
            else:
                startDict[p[0]] = [p]


        tallyNexts = {}

        for startLocation in startDict:
            paths = startDict[startLocation]

            tallyNexts[startLocation] = {}
            for n in self.G.node:
                tallyNexts[startLocation][n] = {}
                for next in self.G[n]:
                    tallyNexts[startLocation][n][next] = 0

            for p in paths:
                for i in range(len(p) - 1):
                    tallyNexts[startLocation][p[i]][p[i+1]] += 1


            for currLoc in tallyNexts[startLocation]:
                numCases = reduce(lambda x,y: x+y, tallyNexts[startLocation][currLoc].values())

                if numCases == 0: # no data so assume all cases equally likely
                    for nextLoc in tallyNexts[startLocation][currLoc]:
                        tallyNexts[startLocation][currLoc][nextLoc] = 1.0 / len(tallyNexts[startLocation][currLoc])
                else:
                    for nextLoc in tallyNexts[startLocation][currLoc]:
                        tallyNexts[startLocation][currLoc][nextLoc] /= (numCases * 1.0)

        # print tallyNexts
        # for key, value in tallyNexts.iteritems():
        #     print key
        #     for k,v in value.iteritems():
        #         print k
        #         print v
        #         print "\n\n"


        return tallyNexts

################# SEARCHING UTILS ########################
    def clearSearchProgress(self):
        for n in self.G.node:
            self.G.node[n]['c'] = 0
        self.itemFoundCount = 0

    def getTotalSearchCount(self):
        return reduce(lambda x,y: x+y, map(lambda x: self.G.node[x]['c'], self.G.node))

    def computeSearchValue(self, weighCounts):
        """ using counts, deduce the value of the search conducted thus far """
        value = 0
        for n in self.G.node:
            if self.G.node[n]['c'] > 0 and self.G.node[n]['r']:
                value += weighCounts(self.G.node[n]['c'])
        return value

    def expDecaySum(self, num):
        sum = 0
        for i in range(num+1):
            sum += self.expDecay(i)

        return sum

    def expDecay(self, num):
        return (1/2.0) ** num



################# SEARCH STRATEGIES ########################

### awesome-sauce. this is a huge accomplishment
### next up: get the system to simulate decisions using this alg
### ponder: do we need to re-generate this table each time, because the counts will keep changing? i suppose you could also batch it... like keep this table until 5+ people have come or something
### TODO: need this strategy to be based on current state of the world. So wouldn't it need to take as input the value function?
### TODO: include start location so P(next | current, start) instead of just P(next | current) to account for directionality, etc...


    def computeWaitingDecisionTable(self, moveModelFromKnownStart, maxTime):
        knownValues = []
        knownDecisions = []

        # print self.G.node

        for t in range(0, maxTime):
            knownValues.append({})
            knownDecisions.append({})

        for n in self.G.node:
            if self.G.node[n]['r']:
                knownValues[0][n] = self.expDecay(self.G.node[n]['c'])
                knownDecisions[0][n] = "Hit"
            else:
                knownValues[0][n] = 0
                knownDecisions[0][n] = "Wait"

        for t in range(1, maxTime):
            for n in self.G.node:

                # base value is if stop right now
                if self.G.node[n]['r']:
                    knownValues[t][n] = self.expDecay(self.G.node[n]['c'])
                else:
                    knownValues[t][n] = 0
                knownDecisions[t][n] = "Hit"



                # see if waiting is better
                expectedValue = 0;


                for next in self.G[n]:
                    # print "-----printing =========" + str(next)
                    # print "known values: "
                    # print knownValues[t-1][next]
                    expectedValue += moveModelFromKnownStart[n][next] * knownValues[t-1][next]
                if expectedValue > knownValues[t][n]:
                    # decision is to WAIT
                    knownValues[t][n] = expectedValue
                    knownDecisions[t][n] = "Wait"

        return {'values': knownValues,
                'decisions': knownDecisions}




    def requestSearchSingleOPT(self, path):
        """
        ALG: omniscient of ind. paths; ping in location of current lowest count
        """
        region = filter(lambda x: self.G.node[x]['r'], path)
        lowestCount = self.lowestCountInRegion(region)
        pingLoc = random.choice(filter(lambda x: self.G.node[x]['c'] == lowestCount, region))
        self.G.node[pingLoc]['c'] += 1
        if self.G.node[pingLoc]['l']:
            self.itemFoundCount += 1

    def requestSearchFirstAvailable(self, path):
        """
        ALG: greedy first encounter
             (go for first cell in search region, regardless of count)
        Hyp: too greedy, will rack up the search count in a lot of places that don't
             need it.
        """

        for n in path:
            if self.G.node[n]['r']:
                self.G.node[n]['c'] += 1
#                print "searching for lost item at %s" % (n,)

                if self.G.node[n]['l']:
                     self.itemFoundCount += 1
 #                   print "found lost item at %s" % (n,)
                break  # only searching one block


    def requestSearchHitorWait(self, path, decisions):
        """
        ALG: Hit-or-Wait Decision Theoretic Alg to compute
             best decision (to hit or wait) as a person walks
             through the region
        Hyp: this is the correct decision-theoretic solution
        """
        maxTime = len(decisions['decisions'])

        # TODO: check for off by one
        for (index, n) in enumerate(path):
            if index >= maxTime:
                break

            if self.G.node[n]['r'] and decisions['decisions'][maxTime - index - 1][n] == "Hit":
                self.G.node[n]['c'] +=1

                print "searching for lost item at %s" % (n,)
                print ".. at index %s and decision point %s" % (index, maxTime-index)


                if self.G.node[n]['l']:
                    self.itemFoundCount += 1

                break





    def requestSearchFirstHitLowestCount(self, path):
        """
           ALG: node counting greedy (go for first cell with lowest count)
           Hyp: search for lowest but will have few actual searchs, lots of walking by
                waiting for that best opportunity which never comes
        """

        lowestCount = self.getLowestActiveCount()
        for n in path:
            if self.G.node[n]['r'] and self.G.node[n]['c'] == lowestCount:
#                print "searching for lost item at %s with count %s" % (n,lowestCount)
                self.G.node[n]['c'] += 1
                if self.G.node[n]['l']:
                     self.itemFoundCount += 1
                break


    def getLowestActiveCount(self):
        region = filter(lambda x: self.G.node[x]['r'], self.G.node)
        return self.lowestCountInRegion(region)

    def lowestCountInRegion(self, region):
        return min(map(lambda x: self.G.node[x]['c'], region))

    def requestSearchFirstHitBelowMedianCount(self, path):
        """
           ALG: node counting favor lows
                -- go for first cell with count lower than the median count
           Hyp: search for low, hit on more searches, but still good amount of walking by
                waiting for good opportunity may not come, but not wasting searches
                where it's low value, either
        """

        medianCount = self.getMedianActiveCount()
        for n in path:
            if self.G.node[n]['r'] and self.G.node[n]['c'] <= medianCount:
#                print "searching for lost item at %s with below median count %s" % (n,medianCount)
                self.G.node[n]['c'] += 1
                if self.G.node[n]['l']:
                     self.itemFoundCount += 1
                break

    def median(self, lst):
        return np.median(np.array(lst))


    def getMedianActiveCount(self):
        region = filter(lambda x: self.G.node[x]['r'], self.G.node)
        return self.median(map(lambda x: self.G.node[x]['c'], region))

##################### END SEARCH STRATEGIES ########################




################### SETUP FUNCTIONS ###################################
    def markLostItem(self, r, c):
        self.G.node[(r,c)]['l'] = True

    def addSearchRegionDown(self, c):
        for r in range(0, self.w):
            self.G.node[(r,c)]['r'] = True


##################### PRINTING FUNCTIONS ###########################
    def printAllPathCount(self):
        counts = {}
        for x in range(0, self.h):
            for y in range(0, self.w):
                counts[(x,y)] = 0
        for p in self.searchPaths:
            for loc in p:
                counts[loc] += 1

        for x in range(0, self.h):
            for y in range(0, self.w):
                print counts[(x,y)],
            print '\n'
        print '\n'

    def printSearcherPath(self, index):
        path = self.searchPaths[index]
        for x in range(0, self.h):
            for y in range(0, self.w):
                if (x,y) in path:
                    print 'w',
                elif self.G.node[(x,y)]['r']:
                    print 'r',
                else:
                    print '-',
            print '\n'
        print '\n'

    def printLostItem(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.G.node[(x,y)]['l']:
                    print 'l',
                elif self.G.node[(x,y)]['r']:
                    print 'r',
                else:
                    print '-',
            print '\n'
        print '\n'

    def printSearchProgress(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.G.node[(x,y)]['c'] != 0:
                    print self.G.node[(x,y)]['c'],
                elif self.G.node[(x,y)]['r']:
                    print 'r',
                else:
                    print '-',
            print '\n'
        print '\n'
