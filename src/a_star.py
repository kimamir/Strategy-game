from queue import PriorityQueue

def get_path(last_visited, current):
    path_length = 0
    while current in last_visited:
        current = last_visited[current] # What square did current come from
        path_length += 1
    return path_length

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(grid, start, end, AI):
    """
    Parameter AI is True if the function is called from the AI's moving algortihm.
    This is important because the function has different return values with different values of 'AI'
    """

    count = 0
    pq = PriorityQueue()
    pq.put((0, count, start))
    last_visited = {}
    g_score = {square: float("inf") for row in grid for square in row} # Shortest distance from start to current
    g_score[start] = 0

    f_score = {square: float("inf") for row in grid for square in row} # Manhattan distance from current to end
    f_score[start] = distance(start.get_location(), end.get_location())

    pq_hash = {start}

    while not pq.empty():
        current = pq.get()[2]
        pq_hash.remove(current) # Synq hash dictionary with priority queue

        if current == end:
            if not AI:
                return get_path(last_visited, end)
            else:
                return getpath(last_visited, end)

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1 # The distance from current to its neighbour

            if temp_g_score < g_score[neighbour]:   # If it's shorter than the currently known distance, update it
                last_visited[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + distance(neighbour.get_location(), end.get_location())
                if neighbour not in pq_hash:
                    count += 1
                    pq.put((f_score[neighbour], count, neighbour))
                    pq_hash.add(neighbour)

    if not AI:
        return float("inf")
    else:
        return None, False


def getpath(last_visited, current):
    path = [current]
    while current in last_visited:
        current = last_visited[current] # What square did current come from
        path.append(current)

    return path, True






