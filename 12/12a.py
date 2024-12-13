from time import perf_counter
from collections import defaultdict

IN_FILE = "12/input.txt"

def calc_fence(start_tile: tuple[int,int], tiles_to_check: list[tuple[int,int]], garden: dict) -> int:
    area = 0
    perimiter = 0
    open_list = [start_tile]
    closed_list = []
    plot = garden[start_tile]

    while len(open_list) > 0:
        check_tile = open_list.pop()
        closed_list.append(check_tile)
        tiles_to_check.remove(check_tile)
        area += 1
        candidates = [
            (check_tile[0] - 1, check_tile[1]),
            (check_tile[0] + 1, check_tile[1]),
            (check_tile[0], check_tile[1] - 1),
            (check_tile[0], check_tile[1] + 1)
        ]
        for candidate in candidates:
            if garden[candidate] is not plot:
                perimiter += 1
            elif candidate not in closed_list and candidate not in open_list:
                open_list.append(candidate)
    
    return area * perimiter

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
                garden[(x,y)] = rows[y][x]
                tiles_to_check.append((x,y))
    
    while len(tiles_to_check) > 0:
        score += calc_fence(tiles_to_check[0], tiles_to_check, garden)

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
