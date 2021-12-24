import math

import search
from itertools import product
import ast
import numpy as np

ids = ["318179660", "316411735"]


class DroneProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        self.grid_size = (len(initial['map']), len(initial['map'][0]))
        hyper_parameter = 1
        penalty = self.grid_size[0]+self.grid_size[1]
        self.map = initial.pop('map')
        clients = initial.pop('clients')
        prev_clients = clients.copy()
        self.client_paths = {}
        self.clients_centroids = {}
        for client, info in prev_clients.items():
            self.client_paths[client] = {}
            self.client_paths[client]['path'] = clients[client].pop('path')
            self.client_paths[client]['len'] = len(self.client_paths[client]['path'])
            clients[client]['loc'] = 0
            self.clients_centroids[client] = tuple([sum(x)/self.client_paths[client]['len'] for x in zip(*self.client_paths[client]['path'])])
            # re-weight of the centroid
            distances_from_centroid = {}
            x_2,y_2 = self.clients_centroids[client]
            for (x_1,y_1) in self.client_paths[client]['path']:
                distances_from_centroid[(x_1,y_1)] = ((x_1-x_2)**2+(y_1-y_2)**2)**0.5
            #scale control
            smoothing_scale = 1
            distances_mean = np.mean(np.array(list(distances_from_centroid.values())))
            if distances_mean != 0:
                smoothing = distances_mean*smoothing_scale
                normalizer = 0
                for point,dist in distances_from_centroid.items():
                    distances_from_centroid[point] += smoothing
                    distances_from_centroid[point] = 1/distances_from_centroid[point]
                    distances_from_centroid[point] = math.exp(distances_from_centroid[point])
                    normalizer += distances_from_centroid[point]
                re_weighted_centroid = [0,0]
                for point,dist in distances_from_centroid.items():
                    distances_from_centroid[point] = dist/normalizer
                for point, prob in distances_from_centroid.items():
                    re_weighted_centroid[0] += point[0]*prob
                    re_weighted_centroid[1] += point[1]*prob
                self.clients_centroids[client] = tuple(re_weighted_centroid)
        initial['clients'] = clients
        drones = initial.pop('drones')
        prev_drones = drones.copy()
        for drone, location in prev_drones.items():
            del drones[drone]
            drones[drone] = {}
            drones[drone]['loc'] = location
            drones[drone]['packages'] = []
        initial['drones'] = drones
        self.penalty_const = hyper_parameter * penalty
        string_state = repr(initial)
        search.Problem.__init__(self, string_state)

    def actions(self, state_node):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        state = ast.literal_eval(state_node)
        drone_to_actions = {}
        for drone, drone_info in state['drones'].items():
            drone_location = drone_info['loc']
            loc_x, loc_y = drone_location
            possible_actions = []
            possible_actions += [('move', drone, (x, y)) for x, y in
                                 [(loc_x - 1, loc_y), (loc_x + 1, loc_y), (loc_x, loc_y - 1), (loc_x, loc_y + 1)]
                                 if self.valid_move(x, y) and self.map[x][y] != 'I']
            for package, package_location in state['packages'].items():
                if package_location == drone_location and len(drone_info['packages']) < 2:
                    possible_actions.append(('pick up', drone, package))
            for client, client_info in state['clients'].items():
                if self.client_paths[client]['path'][client_info['loc']] == drone_location and len(drone_info['packages']) > 0:
                    for package in drone_info['packages']:
                        if package in client_info['packages']:
                            possible_actions.append(('deliver', drone, client, package))
            possible_actions.append(('wait',drone))
            drone_to_actions[drone] = possible_actions
        drone_actions = [drone_actions for drone_actions in drone_to_actions.values()]
        actions = [x for x in product(*drone_actions) if self.check_valid(x)]
        return actions

    def valid_move(self, x, y):
        if x < 0 or y < 0 or x >= self.grid_size[0] or y >= self.grid_size[1]:
            return False
        return True

    def result(self, str_state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        new_state = ast.literal_eval(str_state)
        for act in action:
            if act[0] == 'move':
                new_state['drones'][act[1]]['loc'] = act[2]
            elif act[0] == 'pick up':
                new_state['packages'].pop(act[2])
                new_state['drones'][act[1]]['packages'].append(act[2])
            elif act[0] == 'deliver':
                new_state['drones'][act[1]]['packages'].remove(act[3])
                clients_packages = list(new_state['clients'][act[2]]['packages'])
                clients_packages.remove(act[3])
                new_state['clients'][act[2]]['packages'] = tuple(clients_packages)
        for client, info in new_state['clients'].items():
            info['loc'] = (info['loc'] + 1) % self.client_paths[client]['len']
        return repr(new_state)

    def check_valid(self, action):
        pick_ups = {}
        for move in action:
            if move[0] == 'pick up':
                if move[2] not in pick_ups.keys():
                    pick_ups[move[2]] = move[1]
                else:
                    return False
        return True

    def goal_test(self, str_state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        state = ast.literal_eval(str_state)
        for client, info in state['clients'].items():
            if info['packages']:
                return False
        return True

    def h(self, node):

        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        distances = []
        state = ast.literal_eval(node.state)
        packages_info = state['packages']
        drones_info = state['drones']
        # how many steps to get to the state
        penalty = 0
        # a wait was made but no delivery afterwards, meaning there could be other actions beside the wait
        if node.parent is not None and self.wait_and_no_deliver(node):
            return float('inf')
        # to prefer grids with fewer packages not picked up or delivered
        penalty += len(packages_info) * self.penalty_const * 2
        clients_info = state['clients']
        packages_planned_to = []
        for drone, drone_info in drones_info.items():
            drone_loc = drone_info['loc']
            penalty += 0.5*len(drone_info['packages'])*self.penalty_const
            for package in drone_info['packages']:
                for client, client_info in clients_info.items():
                    if package in client_info['packages']:
                        packages_planned_to.append(package)
                        distances.append(man_dist(drone_loc, self.clients_centroids[client]))
            for client, client_info in clients_info.items():
                for package in client_info['packages']:
                    if package in client_info['packages'] and package in packages_info.keys() and package not in packages_planned_to:
                        package_loc = packages_info[package]
                        distances.append(man_dist(drone_loc, package_loc)+man_dist(package_loc,self.clients_centroids[client]))
        if not distances:
            return penalty*0.9**node.depth
        return -(sum(distances) +penalty)*0.9**node.depth

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""

    def wait_and_no_deliver(self,node):
        if node.parent is not None and node.parent.action is not None:
            for action,prev_action in zip(node.action,node.parent.action):
                if action[0] != 'deliver' and prev_action[0] == 'wait':
                    return True
        return False

def man_dist(tuple_1, tuple_2):
    return sum(abs(a - b) for a, b in zip(tuple_1, tuple_2))


def create_drone_problem(game):
    return DroneProblem(game)
