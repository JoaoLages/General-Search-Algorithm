from Graphs.graphs import Graph
from Graphs.dijkstra import dijkstra
from IO.input import *
from IO.output import *
from Problem.problem import CTSProblem
from Search.a_star_search import *
from copy import deepcopy
import sys


def heuristic(graph, goal_position):  # construct list which indexes are (distance to cask, distance to exit)
    h_dict = {}
    for vertex in graph:
        dijkstra(graph, vertex, graph.get_vertex(goal_position))    # call dijkstra to know the distance
        target1 = graph.get_vertex(goal_position).get_distance()
        for v in graph:     # reset graph
            v.set_distance(sys.maxsize)
            v.set_unvisited()
            v.set_previous(None)
        dijkstra(graph, vertex, graph.get_vertex('EXIT'))  # call dijkstra to know the distance
        target2 = graph.get_vertex('EXIT').get_distance()
        h_dict[vertex.get_id()] = (target1, target2)
        for v in graph:     # reset graph
            v.set_distance(sys.maxsize)
            v.set_unvisited()
            v.set_previous(None)
    return h_dict # return dictionary of the list to be accessed automatically


if __name__ == '__main__':

    # receives the input parameters
    args = get_input()

    # creates an empty graph
    g = Graph()

    # list with all stack's sizes in the facility
    stacks = []

    # list of all casks in the facility
    casks = []

    # Create initial state
    state = []
    state.append(["EXIT", None])  # always starts at EXIT with no cask

    # opens file with graph information
    fp = open(args.filename, "r")

    # reads the input file and fills the graph
    [g, stacks, casks, state, goal_cask_position] = process_file(fp, g, stacks, casks, state, args.cask)
    fp.close()
    # construct a dictionary with the distance to "EXIT" and to goal_cask_position for all nodes in the graph
    h = heuristic(g, goal_cask_position) 

    # define the goal state for the problem
    goal_state = deepcopy(state)
    goal_state[0][1] = args.cask

    # define problem
    p = CTSProblem(tuple(tuple(x) for x in state), tuple(tuple(x) for x in goal_state), g, stacks, casks,
                   goal_cask_position, h)

    # resolve the problem
    result = a_star_search(p)

    # write output to a file
    write_output(result, args)
