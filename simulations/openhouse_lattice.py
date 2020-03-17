import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import numpy
import collections
from functools import reduce
import random

class users:
    def __init__(self):
        self.G = nx.Graph()
    
    def addUser(self, name):
        self.G.add_node(name)

    def getSocialScore(self, user1, user2):
        if self.G.has_edge(user1, user2):
            return 1
        else:
            return 0.5

    def addInteraction(self, user1, user2):
        if self.G.has_edge(user1, user2):
            self.G[user1][user2]['weight'] += 1
        else:
            self.G.add_edge(user1, user2, weight=1)

class latticeSearch:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.G=nx.grid_2d_graph(h, w)
        self.searchPaths = []
        self.itemFoundCount = 0
        self.users = users()

        for x in range(0, h):
            for y in range(0, w):
                self.G.nodes[(x,y)]['v'] = False  # not visited
                self.G.nodes[(x,y)]['r'] = False  # region to search
                self.G.nodes[(x,y)]['c'] = 0      # search value
                self.G.nodes[(x, y)]['user'] = None

################# MODEL MOVEMENT ###########################
    def addSearcherPath(self, user, inputPath):
        self.searchPaths.append((user, inputPath))
        return inputPath
        
    def addSearcherPathsRandom(self, numPaths, users, start, end):
        for i in range(numPaths):
            path = random.choice(list(nx.all_shortest_paths(self.G, start, end)))
            self.searchPaths.append((users[i], path))
        return self.searchPaths

    def createPaths(self, start, end, numPaths):
        paths = []
        for p in range(numPaths):
            path = random.choice(list(nx.all_shortest_paths(self.G, start, end)))
            paths.append(path)
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
            for n in self.G.nodes:
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
           
        return tallyNexts
    
################# SEARCHING UTILS ########################
    def clearSearchProgress(self):
        for n in self.G.nodes:
            self.G.nodes[n]['c'] = 0
        self.itemFoundCount = 0
    
    def clearDeliveryRegions(self):
        for n in self.G.nodes:
            self.G.nodes[n]['user'] = None
            self.G.nodes[n]['r'] = False
            self.G.nodes[n]['c'] = 0

    def getTotalSearchCount(self):
        return reduce(lambda x,y: x+y, map(lambda x: self.G.nodes[x]['c'] > 0, self.G.nodes))

    def computeSearchValue(self, weighCounts):

        """ using counts, deduce the value of the search conducted thus far """
        value = 0
        for n in self.G.nodes:
            if self.G.nodes[n]['c'] > 0 and self.G.nodes[n]['r']:
                # value += weighCounts(self.G.nodes[n]['c'])
                value += self.G.nodes[n]['c']
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


    def computeWaitingDecisionTable(self, moveModelFromKnownStart, helper, maxTime):
        knownValues = []
        knownDecisions = []
        
        # base case
        for t in range(0, maxTime):
            knownValues.append({})
            knownDecisions.append({})

        for n in self.G.nodes:
            requester = self.G.nodes[n]['user']
            if self.G.nodes[n]['r'] and self.G.nodes[n]['c'] == 0:
                # knownValues[0][n] = self.expDecay(self.G.nodes[n]['c'])
                knownValues[0][n] = self.getRelationshipAndSystemScore(helper, requester)
                knownDecisions[0][n] = "Hit"
            else:
                knownValues[0][n] = 0
                knownDecisions[0][n] = "Wait"

        # 
        for t in range(1, maxTime):
            for n in self.G.nodes:
                requester = self.G.nodes[n]['user']
                # base value is if stop right now
                if self.G.nodes[n]['r'] and self.G.nodes[n]['c'] == 0:
                    # knownValues[t][n] = self.expDecay(self.G.nodes[n]['c'])
                    knownValues[t][n] = self.getRelationshipAndSystemScore(helper, requester)
                    knownDecisions[t][n] = "Hit"
                else:
                    knownValues[t][n] = 0
                    knownDecisions[t][n] = "Wait"

                # see if waiting is better
                expectedValue = 0

                for next in self.G[n]:
                    expectedValue += moveModelFromKnownStart[n][next] * knownValues[t-1][next] 

                if expectedValue > knownValues[t][n]:
                    # decision is to WAIT
                    knownValues[t][n] = expectedValue
                    knownDecisions[t][n] = "Wait"

        return {'values': knownValues,
                'decisions': knownDecisions}

        
    def getRelationshipAndSystemScore(self, helper, requester):
        return 0.1 + 0.9*self.users.getSocialScore(requester, helper)


    def requestSearchSingleOPT(self, path):
        """ 
        ALG: omniscient of ind. paths; ping in location of current lowest count
        """
        region = filter(lambda x: self.G.nodes[x]['r'] and self.G.nodes[x]['c'] == 0, path[1])            
        choices = list(map(
            lambda x: (x, self.getRelationshipAndSystemScore(path[0], self.G.nodes[x]['user'])), region
            ))

        def sortSecond(val): 
            return val[1] 
        
        choices.sort(key = sortSecond, reverse = True)

        if len(choices) != 0:
            pingLoc = choices[0][0]
            self.G.nodes[pingLoc]['c'] = choices[0][1]

    def requestSearchFirstAvailable(self, path):
        """
        ALG: greedy first encounter 
             (go for first cell in search region, regardless of count)
        Hyp: too greedy, will rack up the search count in a lot of places that don't 
             need it. 
        """

        for n in path[1]:
            if self.G.nodes[n]['r'] and self.G.nodes[n]['c'] == 0:
                self.G.nodes[n]['c'] += self.getRelationshipAndSystemScore(path[0], self.G.nodes[n]['user'])
#                print "completing delivery at %s" % (n,)
                break  # only searching one block


    def requestSearchHitorWait(self, path, decisions):
        """
        ALG: Hit-or-Wait Decision Theoretic Alg to compute
             best decision (to hit or wait) as a person walks 
             through the region
        Hyp: this is the correct decision-theoretic solution
        """
        maxTime = len(list(decisions.values())[0]['decisions'])

        # TODO: check for off by one
        for (index, n) in enumerate(path[1]):
            if index >= maxTime:
                break
            if self.G.nodes[n]['r'] and decisions[path[0]]['decisions'][maxTime - index - 1][n] == "Hit":
                self.G.nodes[n]['c'] += decisions[path[0]]['values'][maxTime - index - 1][n]
                self.users.addInteraction(path[0], self.G.nodes[n]['user'])

                # print("completing delivery at %s" % (n,))
                # print(".. at index %s and decision point %s" % (index, maxTime-index))

                break
    
    def getLowestActiveCount(self):
        region = filter(lambda x: self.G.nodes[x]['r'], self.G.nodes)
        return self.lowestCountInRegion(region)
        
    def lowestCountInRegion(self, region):
        return min(map(lambda x: self.G.nodes[x]['c'], region))

    def median(self, lst):
        return np.median(np.array(lst))


    def getMedianActiveCount(self):
        region = filter(lambda x: self.G.nodes[x]['r'], self.G.nodes)
        return self.median(map(lambda x: self.G.nodes[x]['c'], region))

##################### END SEARCH STRATEGIES ########################




################### SETUP FUNCTIONS ###################################
    
    def addDeliveryRegion(self, user, x, y):
        self.G.nodes[(x, y)]['user'] = user
        self.G.nodes[(x,y)]['r'] = True

    def addSearchRegionDown(self, c):
        for r in range(0, self.w):
            self.G.nodes[(r,c)]['r'] = True


##################### PRINTING FUNCTIONS ###########################
    def printAllPathCount(self):
        counts = {}
        for x in range(0, self.h):
            for y in range(0, self.w):
                counts[(x,y)] = 0
        for p in self.searchPaths:
            for loc in p[1]:
                counts[loc] += 1
                
        for x in range(0, self.h):
            for y in range(0, self.w):
                print(counts[(x,y)], end="\t"),
            print('\n')
        print('\n')
        
    def printSearcherPath(self, index):
        path = self.searchPaths[index][1]
        for x in range(0, self.h):
            for y in range(0, self.w):
                if (x,y) in path:
                    print('w', end="\t"),
                elif self.G.nodes[(x,y)]['r']:
                    print(self.G.nodes[(x,y)]['user'], end="\t"),
                else:
                    print('-', end="\t"),
            print('\n')
        print('\n')

    def printLostItem(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.G.nodes[(x,y)]['r']:
                    print(self.G.nodes[(x,y)]['user'], end="\t"),
                else:
                    print('-', end="\t"),
            print('\n')
        print('\n')
    
    def printSearchProgress(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.G.nodes[(x,y)]['c'] != 0:
                    print(round(self.G.nodes[(x,y)]['c'], 2), end="\t"),
                elif self.G.nodes[(x,y)]['r']:
                    print(self.G.nodes[(x,y)]['user'], end="\t"),
                else:
                    print('-', end="\t"),
            print('\n')
        print('\n')
