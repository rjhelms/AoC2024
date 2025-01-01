from time import perf_counter
from collections import defaultdict
from itertools import permutations

IN_FILE = "12/input.txt"

WALK_VECTORS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # up, right, down, left


def calc_fence(
    start_tile: tuple[int, int], tiles_to_check: list[tuple[int, int]], garden: dict
) -> int:
    area = 0
    perimiter = 0
    open_list = [start_tile]
    closed_list = []
    plot = garden[start_tile]

    # key is an index to WALK_VECTORS, value is a list of 4-tuples representing an edge facing that direction - x_start,y_start,x_end,y_end
    edge_tiles = defaultdict(list)

    while len(open_list) > 0:
        check_tile = open_list.pop()
        closed_list.append(check_tile)
        tiles_to_check.remove(check_tile)
        area += 1
        for i in range(len(WALK_VECTORS)):
            candidate = (
                check_tile[0] + WALK_VECTORS[i][0],
                check_tile[1] + WALK_VECTORS[i][1],
            )
            if garden[candidate] is not plot:
                edge_tiles[i].append(
                    (check_tile[0], check_tile[1], check_tile[0], check_tile[1])
                )
            elif candidate not in closed_list and candidate not in open_list:
                open_list.append(candidate)

    edges = 0
    for key in edge_tiles:
        found_merge = True
        while found_merge:
            found_merge = False
            new_edges = edge_tiles[key]
            merge_vector = WALK_VECTORS[(key + 1) % 4]
            for pair in permutations(edge_tiles[key], 2):
                if (
                    pair[0][2] + merge_vector[0] == pair[1][0]
                    and pair[0][3] + merge_vector[1] == pair[1][1]
                ):
                    new_edges.remove(pair[0])
                    new_edges.remove(pair[1])
                    new_edges.append((pair[0][0], pair[0][1], pair[1][2], pair[1][3]))
                    found_merge = True
                    break
            edge_tiles[key] = new_edges
        edges += len(edge_tiles[key])

    return area * edges


if __name__ == "__main__":
    start_time = perf_counter()

    max_y = 0
    max_x = 0
    score = 0
    garden = defaultdict(lambda: "")
    tiles_to_check = []

    with open(IN_FILE) as f:
        rows = f.readlines()
        max_y = len(rows)
        max_x = len(rows[0].strip())
        for y in range(len(rows)):
            for x in range(len(rows[y].strip())):
                garden[(x, y)] = rows[y][x]
                tiles_to_check.append((x, y))

    while len(tiles_to_check) > 0:
        score += calc_fence(tiles_to_check[0], tiles_to_check, garden)

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
