from Utils.utils import *
from Graphs.graphs import *
from Problem.problem import assign_h1, assign_h2


class Node:

    # A node in our search tree, that we use for our search algorithm

    def __init__(self, state, parent=None, action=None, path_cost=0, heuristic=0):
        # Create a search tree Node, derived from a parent by an action.
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, node):  # compare nodes by path cost
        return self.path_cost < node.path_cost

    def expand(self, problem):  # return reachable nodes from the actions possible
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):  # return Node reachable from a certain action 
        next = problem.result(self.state, action)
        return Node(next, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next))

    def solution(self): # return all the actions and path_costs to get to the goal state
        solution = []
        prev_cost = 0
        for node in self.path()[1:]:
            solution.append([node.action, node.path_cost - prev_cost])
            prev_cost = node.path_cost
        return solution

    def path(self):
        # Return a list of nodes forming the path from the root to this node.
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def uniform_cost_search(problem, f):
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = PriorityQueue(min, f)  # organize frontier by f value

    frontier.append(node)
    explored = set()  # put explored nodes in a set for faster search
    while frontier:  # while frontier not empty, continue the search
        node = frontier.pop()
        if node.state not in explored:  # if node not in explored, explore it
            explored.add(node.state)
            if problem.goal_test(node.state):  # check goal condition
                return node
            for child in node.expand(problem):  # add child nodes to frontier if not explored
                if child not in explored:
                    child.heuristic = assign_h1(problem, child.state) # calculate heuristic
                    frontier.append(child)
    return None


def a_star_search(problem):
    return uniform_cost_search(problem, lambda node: node.path_cost + node.heuristic)


