from time import perf_counter
from functools import cache
from collections import defaultdict

# solution is the same for both parts - set MAX_ITERATIONS appropriately
MAX_ITERATIONS = 75

IN_FILE = "11/input.txt"


@cache
def blink(value: int) -> list[int]:
    if value == 0:
        return [1]
    string = str(value)
    if len(string) % 2 == 0:
        split = len(string) // 2
        return [int(string[:split]), int(string[split:])]
    else:
        return [value * 2024]


if __name__ == "__main__":
    start_time = perf_counter()

    # order of stones doesn't matter - so can represent them as a dictionary
    # key is number and value is count of stones bearing that number

    stones = defaultdict(int)

    with open(IN_FILE) as f:
        for stone in f.read().split():
            stones[int(stone)] += 1

    iter = 0
    while iter < MAX_ITERATIONS:
        new_stones = defaultdict(int)
        for stone in stones:
            result = blink(stone)
            for num in result:
                new_stones[num] += stones[stone]
        stones = new_stones
        iter += 1

    score = 0
    for stone in stones:
        score += stones[stone]

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
