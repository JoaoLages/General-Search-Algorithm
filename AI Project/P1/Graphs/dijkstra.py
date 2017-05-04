import heapq


def dijkstra(aGraph, start, target):

    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    #print(len(unvisited_queue))
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        #print(len(unvisited_queue))
        uv = heapq.heappop(unvisited_queue)
        #print(uv[1].get_id())
        current = uv[1]  # <- this is a vertex
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)
