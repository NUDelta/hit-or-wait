# Temp database before I persist somewhere
"""
    The idea here is to mock a simple scenario and see if hit-or-wait makes the right decisions.
    - To see the example states look at fixtures/example_states.json

    Approach:
    - I first decided the live user routes.
    - Then I placed some tasks, with varying importance scores
    - Routes were mocked to lead to certain state transition probabilities I decided
"""
class Database:
    def __init__(self):
        # save all routes
        # for each user, array of route information (lat-lng pairs with time)
        self.routes = {
            "4": [
                # create these state transitions through routes: [4->1->5->4->1->2]
                # ^ to test that certain state transition probabilities are created
                # { 4->1 : 1, 1->5 : 0.5, 1->2 : 0.5, 5->4 : 1 }
                {
                    "time": 1583941000,
                    # state 4
                    "lat": 42.046,
                    "lng": -87.680
                },
                {
                    "time": 1583942000,
                    # state 1
                    "lat": 42.048,
                    "lng": -87.680
                },
                {
                    "time": 1583943000,
                    # state 5
                    "lat": 42.046,
                    "lng": -87.677
                },
                {
                    "time": 1583944000,
                    # state 4
                    "lat": 42.045,
                    "lng": -87.681
                },
                {
                    "time": 1583945000,
                    # state 1
                    "lat": 42.053,
                    "lng": -87.691
                },
                {
                    "time": 1583946000,
                    # state 2
                    "lat": 42.055,
                    "lng": -87.680
                },
            ],
            "2": [
                {
                    "time": 1583946000,
                    "lat": 42.042,
                    "lng": -87.690
                },
            ]
        }
        # map of user_id : user_info (just name for now)
        self.users = {
            "1": {
                "name": "Alice"
            },
            "2": {
                "name": "Bob"
            },
            "3": {
                "name": "Cooper"
            },
            "4": {
                "name": "Morty"
            }
        }
        # computed policies.
        # should be a map of user_id : decisions
        # decisions should be a map of state_id : policy (hit or wait"
        self.decision_table = {

        }
        # separate into two maps: active and past.
        # each map has task_id : info
        self.tasks = {
            "active": {
                "123": {
                    "requester": "1",
                    "location": { # state 4
                        "lat": 42.042,
                        "lng": -87.690
                    }
                },
                "456": {
                    "requester": "2",
                    "location": { # state 5
                        "lat": 42.042,
                        "lng": -87.670
                    }
                },
                "789": {
                    "requester": "3",
                    "location": { # state 2
                        "lat": 42.055,
                        "lng": -87.680
                    }
                }
            },
            "past": {}
        }
        #
        self.relationships = {
            "4-1": {
                "friendship": 0
            },
            "4-2": {
                "friendship": 0.5
            },
            "4-3": {
                "friendship": 1
            }
        }

