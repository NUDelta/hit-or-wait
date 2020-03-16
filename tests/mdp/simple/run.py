import json
import matplotlib.pyplot as plt
from matplotlib import patches
import random
from mdp.SynergyHitOrWait import SynergyHitOrWait
from .database import Database

with open("tests/mdp/simple/example_states.json") as data:
    campus_states = json.load(data)

database = Database()

show = SynergyHitOrWait(campus_states, database)
route1 = [
    {
        "lat": 42.042, # state 4
        "lng": -87.691
    },
    {
        "lat": 42.044, # still state 4
        "lng": -87.691
    },
    {
        "lat": 42.050, # state 1
        "lng": -87.690
    },
    {
        "lat": 42.055, # state 2
        "lng": -87.680
    },
]
decisions = []
helper_id = "4"
for loc in route1:
    decisions.append(show.get_decision(loc["lat"], loc["lng"], helper_id))

# TODO: show that Cooper's task was assigned
assert(decisions == ['Wait', 'Wait', 'Wait', 'Hit'])




# def convert_region_to_list_of_points(campus_state_vals):
#     region = [[loc["lng"], loc["lat"]] for loc in campus_state_vals["region"]]
#     campus_state_vals["region"] = region
#     return campus_state_vals
#

#
# campus_states = {
#     key:convert_region_to_list_of_points(val) for key, val in campus_states.items()
# }

# for campus_state_vals in campus_states.values():
#     plt.gca().add_patch(patches.Polygon(campus_state_vals["region"], color=[random.random() for _ in range(0, 3)]))
# plt.axis('equal')
# plt.show()