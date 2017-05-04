import argparse
from Cask.cask import Cask
from Stack.stack import Stack


def get_input():
    parser = argparse.ArgumentParser(description='Input information.')
    parser.add_argument("filename")
    parser.add_argument("cask")

    return parser.parse_args()

def process_file(file, graph, stack_list, cask_list, state, goal_cask):
    # reads each line from the input file and processes it accordingly
    aux_stacklist = []
    for line in file:

        # splits the received line in words separated by blank space
        words = line.split()

        # case when reading cask info
        if line[0] == 'C':
            cask_list.append(Cask(words[0], float(words[1]), float(words[2])))
            state.append([words[0], 0])
        # case when reading stack info
        elif line[0] == 'S':
            graph.add_vertex(words[0])
            stack_list.append(Stack(words[0], float(words[1])))
            string = words[0]
            for cask in words[2:]:
                if cask == goal_cask:
                    goal_cask_position = words[0]
                string += " " + cask
            aux_stacklist.append(string)
        # case when reading edges info
        elif line[0] == 'E':
            graph.add_edge(words[1], words[2], float(words[3]))

    for cask_state in state[1:]:
        for stack in aux_stacklist:
            cask = stack.split()
            for pos, i in enumerate(reversed(cask)):
                if i == cask_state[0]:
                    cask_state[0] = cask[0]
                    cask_state[1] = pos + 1
                    break

    to_remove = []
    for i, cask in enumerate(state[1:]):
        if cask[0][0] == "C": #it's an unassigned cask
            to_remove.append(i+1)
    for i in reversed(to_remove):
        del state[i]
        del cask_list[i-1]
    return graph, stack_list, cask_list, state, goal_cask_position
