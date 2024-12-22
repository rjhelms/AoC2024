from time import perf_counter
from collections import defaultdict
from heapq import heappop, heappush
from copy import copy

IN_FILE = "20/input.txt"

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

MAX_X = 0
MAX_Y = 0

SKIP_LENGTH = 20
TARGET_SAVINGS = 100


class MapDict(dict):
    def __missing__(self, key):
        if key[0] < 0 or key[1] < 0 or key[0] > MAX_X or key[1] > MAX_Y:
            return False
        return True


WORLD_MAP = MapDict()


def get_neighbours(
    coords: tuple[int], world_map: MapDict, open: bool
) -> list[tuple[int]]:
    neighbour_list = []
    for direction in DIRECTIONS:
        candidate = tuple(map(sum, zip(coords, direction)))
        if world_map[candidate] and open:
            neighbour_list.append(candidate)
        elif not world_map[candidate] and not open:
            neighbour_list.append(candidate)
    return neighbour_list


def manhattan(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def A_star(start, goal, map):
    g_score = defaultdict(lambda: float("inf"))
    f_score = defaultdict(lambda: float("inf"))
    came_from = {}
    g_score[start] = 0
    f_score[start] = manhattan(start, goal)
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

        for neighbour in get_neighbours(current, map, True):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + manhattan(neighbour, goal)
                if neighbour not in [x[1] for x in open_set]:
                    heappush(open_set, (f_score[neighbour], neighbour))
    return False


if __name__ == "__main__":
    start_time = perf_counter()

    start_pos = (0, 0)
    end_pos = (0, 0)

    with open(IN_FILE) as f:
        lines = f.readlines()
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    WORLD_MAP[(x, y)] = False
                elif lines[y][x] == "E":
                    end_pos = (x, y)
                elif lines[y][x] == "S":
                    start_pos = (x, y)

    MAX_X = x
    MAX_Y = y

    path = A_star(start_pos, end_pos, WORLD_MAP)
    path.append(start_pos)  # need to add the starting tile
    score = 0

    for i in range(len(path)):
        if i % 100 == 0:
            print(".", end="", flush=True)
        for y in range(-SKIP_LENGTH, SKIP_LENGTH + 1):
            for x in range(-SKIP_LENGTH, SKIP_LENGTH + 1):
                candidate = tuple(map(sum, zip(path[i], (x, y))))
                if (
                    manhattan(path[i], candidate) <= SKIP_LENGTH
                    and WORLD_MAP[candidate]
                ):
                    if candidate in path[:i]:
                        savings = i - path.index(candidate)
                        savings -= manhattan(path[i], candidate)
                        if savings >= TARGET_SAVINGS:
                            score += 1

    print()
    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
