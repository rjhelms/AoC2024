from time import perf_counter
from collections import defaultdict
from heapq import heappop, heappush

IN_FILE = "16/input.txt"

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
WALL_MAP = []
TURN_COST = 1000
MOVE_COST = 1


# nodes represented as 3 element tuples - first two are position, third is index to direction
def get_neighbours(node):
    """Returns list of neighbours, each as a tuple (Node, cost)"""
    neighbour_list = []
    forward_position = (
        node[0] + DIRECTIONS[node[2]][0],
        node[1] + DIRECTIONS[node[2]][1],
        node[2],
    )
    if (forward_position[0], forward_position[1]) not in WALL_MAP:
        neighbour_list.append((forward_position, MOVE_COST))
    left_turn = (node[0], node[1], (node[2] - 1) % 4)
    right_turn = (node[0], node[1], (node[2] + 1) % 4)
    neighbour_list.append((left_turn, TURN_COST))
    neighbour_list.append((right_turn, TURN_COST))
    return neighbour_list


def heuristic(start_node, goal_pos):
    return abs(start_node[0] - goal_pos[0]) + abs(start_node[1] - goal_pos[1])


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
            return g_score[current]

        for neighbour in get_neighbours(current):
            tentative_g_score = g_score[current] + neighbour[1]
            if tentative_g_score < g_score[neighbour[0]]:
                came_from[neighbour[0]] = current
                g_score[neighbour[0]] = tentative_g_score
                f_score[neighbour[0]] = tentative_g_score + heuristic(
                    neighbour[0], goal
                )
                if neighbour[0] not in [x[1] for x in open_set]:
                    heappush(open_set, (f_score[neighbour[0]], neighbour[0]))
    return False


if __name__ == "__main__":
    start_time = perf_counter()
    goal = (0, 0)
    start_node = (0, 0, 0)
    with open(IN_FILE) as f:
        lines = f.readlines()
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#":
                    WALL_MAP.append((x, y))
                elif lines[y][x] == "E":
                    goal = (x, y)
                elif lines[y][x] == "S":
                    start_node = (x, y, 0)

    print(A_star(start_node, goal))
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
