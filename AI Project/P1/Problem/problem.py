from copy import deepcopy


class Problem(object):

    """The abstract class for a formal problem. All methods should be implemented for a specific problem"""

    def __init__(self, initial, goal=None):
        """ constructor defines a initial and goal state"""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result should be returned in a tuple. """
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. """
        raise NotImplementedError

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. The default
        method assumes that the cost between states is only 1."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value."""
        raise NotImplementedError


class CTSProblem(Problem):  # define a specific problem
    def __init__(self, initial, goal, graph, stack_list, cask_list, goal_cask_position, heuristic):
        Problem.__init__(self, initial, goal) 
        self.graph = graph
        self.stack_list = stack_list
        self.cask_list = cask_list
        self.goal_cask_position = goal_cask_position
        self.heuristic = heuristic
        for i, cask in enumerate(self.cask_list):
            if cask.get_name() == goal[0][1]:
                index = i + 1
                break
        self.goal_cask_index = index

    def get_goalcaskposition(self):
        return self.goal_cask_position

    def get_graph(self):
        return self.graph

    def got_goalcask(self, state):
        return state[0][1] == self.goal[0][1]

    def actions(self, state):  # receives state, returns (action, cask/edge , edge)
        actions = []
        if state[0][0][0] == "S":  # CTS is in a stack
            if state[0][1] is not None:  # loaded, can unload
                stack_size = 0
                for s in self.stack_list:  # finds stack size that we want to unload the cask into
                    if s.get_name() == state[0][0]:
                        stack_size = s.get_size()
                        break
                for i, st in enumerate(state[1:]):  # gets available space in stack
                    if st[0] == state[0][0] and st[1] != 0:
                        stack_size -= self.cask_list[i].get_size()
                for c in self.cask_list:  # finds cask size
                    if c.get_name() == state[0][1]:
                        #print("cask_size: " + str(c.get_size()) + " stack_size: " + str(stack_size))
                        if c.get_size() <= stack_size:  # possible to unload
                            actions.append(["unload", c.get_name(), state[0][0]])  # add action 
                        break
            else:  # unloaded, can load
                for i, st in enumerate(state[1:]):  # find cask to load
                    if st[0] == state[0][0] and st[1] == 1:  # cask to load
                        actions.append(["load", self.cask_list[i].get_name(), state[0][0]])  # add action
                        break

        neighbours = self.graph.get_neighbours(state[0][0])  # find neighbours in graph to move CTS
        for name in neighbours.get_list_connections():
            actions.append(["move", state[0][0], name])  # add action
        return tuple(tuple(x) for x in actions)

    def result(self, state, action):  # receives state and action, returns new state
        state = list(list(x) for x in state)
        new_state = deepcopy(state)
        if action[0] == "move":  # action is move
            new_state[0][0] = action[2]  # update CTS position
            if state[0][1] is not None:  # CTS loaded, update cask position too
                for i, cask_position in enumerate(state[1:]):
                    if cask_position[0] == state[0][0] and cask_position[1] == 0:  # find matching cask
                        new_state[i + 1][0] = action[2]  # update cask position
                        break
        elif action[0] == "load":  # action is load
            new_state[0][1] = action[1]  # update CTS load
            for i, st in enumerate(state[1:]):
                if st[0] == action[2]:
                    new_state[i + 1][1] -= 1  # lower the level of casks in stack
        elif action[0] == "unload":  # action is unload
            new_state[0][1] = None  # update CTS load
            for i, st in enumerate(state[1:]):
                if st[0] == action[2]:
                    new_state[i + 1][1] += + 1  # increase the id of casks in stack
        return tuple(tuple(x) for x in new_state)

    def goal_test(self, state):  # return True if goal is reached
        return state[0][0] == self.goal[0][0] and state[0][1] == self.goal[0][1]

    def path_cost(self, c, state1, action, state2):  # return path cost so far
        if action[0] == "unload" or action[0] == "load":  # costs of unload/load
            for cask in self.cask_list:
                if cask.get_name() == action[1]:
                    return float(c + 1 + cask.get_weight())
        else:  # costs of move
            cost = 0  # just not to create problems (remove in final version)
            for v in self.graph:
                for w in v.get_connections():
                    if v.get_id() == action[1] and w.get_id() == action[2]:  # find corresponding edge in graph
                        cost = float(v.get_weight(w))  # add edge cost
                        break
            if state1[0][1] is not None:  # CTS is loaded
                for cask in self.cask_list:
                    if cask.get_name() == state1[0][1]:  # find corresponding cask
                        cost *= float(cask.get_weight() + 1)  # add additional cost
                        break
            return float(c + cost)

    def value(self, state):  # not needed
        return 0


def assign_h1(problem, state):  # 1st heuristic

    if state[0][1] is None:  # has no cask => wants to go to cask position
        return problem.heuristic[state[0][0]][0] + problem.heuristic[problem.goal_cask_position][1]

    elif problem.got_goalcask(state):  # has cask goal => wants to go to exit
        return problem.heuristic[state[0][0]][1]

    else: # has another cask => maintain value for heuristic to be admissible and consistent
        return problem.heuristic[problem.goal_cask_position][1]


def assign_h2(problem, state):  # 2nd heuristic
    h = 0
    for i, s in enumerate(state[1:]):  # find casks above goal cask and add their cost
        if s[0] == problem.goal_cask_position and s[1] < state[problem.goal_cask_index][1]:
            h += 2 + 2 * problem.cask_list[i-1].get_weight()

    if state[problem.goal_cask_index][1] != 0:   # add cost of goal cask
        h += 1 + problem.cask_list[problem.goal_cask_index - 1].get_weight()
    return h