def write_output(result, args):
    fp = open(args.filename.replace('.dat', '_' + args.cask + '.out'), 'w')
    for action in result.solution():
        line = ""
        action = str(action)
        for i, c in enumerate(action):
            if not (c == "[" or c == "]" or c == "(" or c == ")" or c == "'" or (c == "," and action[i+1] == " ")):
                line += c
        fp.write(line + "\n")
    fp.write(str(result.path_cost))
    fp.close()
