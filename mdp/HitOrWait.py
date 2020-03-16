import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import numpy
import collections
from functools import reduce
import random

class HitOrWait:
    def __init__(self):
        self.G = nx.Graph()

    def add_state(self, id):
        self.G.add_node(id, tasks=[])

    def add_neighbors(self, state_id, neighbors):
        for neighbor in neighbors:
            self.G.add_edge(state_id, neighbor, prob=0)

    def add_task(self, node, task_id):
        self.G.nodes[node]["tasks"].append(task_id)

    ################# MODEL MOVEMENT ###########################

    def compute_movement_model(self, state_transitions):
        """
            Input: Dict[currentLocation][nextLocation] = num_transitions
            Returns: Dict[currentLocation][nextLocation] = probability
            Assumes:
            - When no paths through s in data, assume P(s->s') = 1 / len(s')
        """
        st = state_transitions
        for state in st.keys():
            total = 0
            num_neighbors = len(list(self.G.neighbors(state)))

            for other_state in st[state]:
                total += st[state][other_state]

            if total == 0:
                for other_state in self.G.neighbors(state):
                    self.G[state][other_state]["prob"] = 1 / num_neighbors
            else:
                for other_state in st[state]:
                    self.G[state][other_state]["prob"] = st[state][other_state] / total

    ################# SEARCH STRATEGIES ########################
    ### TODO: include start location so P(next | current, start) instead of just P(next | current) to account for directionality, etc...

    def compute_decisions(self, value_function, max_time):
        known_values = []
        known_decisions = []

        for t in range(0, max_time):
            known_values.append({})
            known_decisions.append({})

        # base case
        for n in self.G.nodes:
            if len(self.G.nodes[n]['tasks']) == 0:
                known_values[0][n] = 0
                known_decisions[0][n] = "Wait"
            else:
                # TODO: how to deal with multiple tasks in same node?
                first_task = self.G.nodes[n]['tasks'][0]
                known_values[0][n] = value_function(first_task)
                known_decisions[0][n] = "Hit"


        for t in range(1, max_time):
            for n in self.G.nodes:
                # base value is to hit right now
                if len(self.G.nodes[n]['tasks']) != 0:
                    # TODO: how to deal with multiple tasks?
                    first_task = self.G.nodes[n]['tasks'][0]
                    known_values[t][n] = value_function(first_task)
                    known_decisions[t][n] = "Hit"
                else:
                    known_values[t][n] = 0
                    known_decisions[t][n] = "Wait"

                # see if waiting is better
                expected_value = 0

                for next in self.G[n]:
                    expected_value += self.G[n][next]["prob"] * known_values[t - 1][next]

                if expected_value > known_values[t][n]:
                    # decision is to WAIT
                    known_values[t][n] = expected_value
                    known_decisions[t][n] = "Wait"

        return known_decisions[max_time - 1]

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

    ##################### END SEARCH STRATEGIES ########################
