from .HitOrWait import HitOrWait
import networkx as nx
from shapely.geometry import Polygon, Point

class SynergyHitOrWait:
    def __init__(self, state_representation, database):
        self.how = HitOrWait()
        self.states = self.make_states_polygons(state_representation)
        self.add_states_to_how(state_representation)
        self.evanston_bounds = self.get_evanston_bounds()

        self.routes = database.routes
        self.active_tasks = database.tasks["active"]
        self.users = database.users
        self.relationships = database.relationships

        # TODO: create decisions for all users
        helper_id = list(self.users.keys())[-1]
        st = self.compute_state_transitions(self.routes, helper_id)
        self.how.compute_movement_model(st)
        self.assign_tasks(self.active_tasks)
        database.decision_table[helper_id] = self.compute_policy(helper_id)
        self.decision_table = database.decision_table

    def add_states_to_how(self, state_representation):
        for state in state_representation:
            self.how.add_state(state)
        for state in state_representation:
            self.how.add_neighbors(state, state_representation[state]["neighbors"])

    def get_state(self, lat, lng):
        pt = Point(lng, lat)
        for state in self.states.keys():
            if self.states[state]["polygon"].contains(pt):
                return state

        return False

    def compute_system_and_social_score(self, helper_id, task_id):
        requester_id = self.active_tasks[task_id]["requester"]
        relationship_id = helper_id + "-" + requester_id
        if relationship_id not in self.relationships:
            relationship_id = requester_id + "-" + helper_id
        return self.relationships[relationship_id]["friendship"]*0.9 + 0.1

    def assign_tasks(self, tasks):
        #TODO: deal with multiple tasks in one location
        #TODO: deal with adding task to multiple states based on notification radius

        for key, _ in tasks.items():
            loc = tasks[key]["location"]
            state = self.get_state(loc["lat"], loc["lng"])
            if state == False:
                # TODO: throw error, there is an illegal task!
                pass
            self.how.add_task(state, key)

    def compute_policy(self, user_id):
        # TODO: change max_time
        value_function_for_one_user = \
            lambda x : self.compute_system_and_social_score(user_id, x)
        return self.how.compute_decisions(value_function_for_one_user, 2)

    def compute_state_transitions(self, routes, user_id):
        """
            Assumes:
            - Routes per user are already sorted by time
            - If consecutive times of route locations are greater than route_time_threshold, it is a separate route
        """

        route_time_threshold = 2000 # Unix Time

        state_transitions = {}
        for i in range(0, len(routes[user_id]) - 1):
            curr_loc = routes[user_id][i]
            next_loc = routes[user_id][i+1]
            if next_loc["time"] - curr_loc["time"] > route_time_threshold:
                continue
            curr_state = self.get_state(curr_loc["lat"], curr_loc["lng"])
            next_state = self.get_state(next_loc["lat"], next_loc["lng"])

            if curr_state != False and next_state != False:
                if curr_state not in state_transitions:
                    state_transitions[curr_state] = {}
                if next_state not in state_transitions[curr_state]:
                    state_transitions[curr_state][next_state] = 0
                state_transitions[curr_state][next_state] += 1

        return state_transitions

    def get_decision(self, lat, lng, user_id):
        state = self.get_state(lat, lng)
        if state == False:
            return "Wait"
        return self.decision_table[user_id][state]

    def getRelationshipAndSystemScore(self, helper, requester):
        return 0.1 + 0.9*self.users.getSocialScore(requester, helper)

    ############# HELPERS ###################
    def add_polygon(self, campus_state_vals):
        pts = [[loc["lng"], loc["lat"]] for loc in campus_state_vals["region"]]
        campus_state_vals["polygon"] = Polygon(pts)
        return campus_state_vals

    def make_states_polygons(self, campus_states):
        return {
            key: self.add_polygon(val) for key, val in campus_states.items()
        }

    def get_evanston_bounds(self):
        # [lng, lat]
        left_top = [-87.692412, 42.063650]
        right_top = [-87.667343, 42.063650]
        right_bottom = [-87.667343, 42.040201]
        left_bottom = [-87.692412, 42.040201]

        return Polygon([left_top, left_bottom, right_bottom, right_top])



