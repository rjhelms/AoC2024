from time import perf_counter
from collections import defaultdict
from heapq import heappop, heappush

IN_FILE = "18/input.txt"

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

MAX_X = 70
MAX_Y = 70


class MapDict(dict):
    def __missing__(self, key):
        if key[0] < 0 or key[1] < 0 or key[0] > MAX_X or key[1] > MAX_Y:
            return False
        return True


WORLD_MAP = MapDict()


def get_neighbours(coords: tuple[int]) -> list[tuple[int]]:
    neighbour_list = []
    for direction in DIRECTIONS:
        candidate = tuple(map(sum, zip(coords, direction)))
        if WORLD_MAP[candidate]:
            neighbour_list.append(candidate)
    return neighbour_list


def heuristic(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def A_star(start, goal):
    g_score = defaultdict(lambda: float("inf"))
    f_score = defaultdict(lambda: float("inf"))
    came_from = {}
    g_score[start] = 0
    f_score[start] = heuristic(start, goal)
    open_set = []
    heappush(open_set, (f_score[start], start))

    while len(open_set) > 0:
        current = heappop(open_set)[1]
        if current[0] == goal[0] and current[1] == goal[1]:
            path = []
            while current is not start:
                path.append(current)
                current = came_from[current]
            return path

        for neighbour in get_neighbours(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(neighbour, goal)
                if neighbour not in [x[1] for x in open_set]:
                    heappush(open_set, (f_score[neighbour], neighbour))
    return False


if __name__ == "__main__":
    start_time = perf_counter()

    start_pos = (0, 0)
    end_pos = (MAX_X, MAX_Y)

    drops = []
    with open(IN_FILE) as f:
        for line in f:
            drops.append(tuple(int(x) for x in line.split(",")))

    path = A_star(start_pos, end_pos)
    i = 0
    while True:
        WORLD_MAP[drops[i]] = False
        if drops[i] in path:
            path = A_star(start_pos, end_pos)
            if path == False:
                break
        i += 1

    print(drops[i])
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
