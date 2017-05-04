from Graphs.graphs import *
from IO.input import *
from IO.output import *
from Problem.problem import CTSProblem
from Search.uniform_cost_search import *
from copy import deepcopy
import time


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

    # define the goal state for the problem
    goal_state = deepcopy(state)
    goal_state[0][1] = args.cask

    # define the problem
    p = CTSProblem(tuple(tuple(x) for x in state), tuple(tuple(x) for x in goal_state), g, stacks, casks, None, None)

    # resolve the problem
    result = search(p)

    # write output to file 
    write_output(result, args)
