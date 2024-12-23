from time import perf_counter
from collections import defaultdict
from itertools import combinations

IN_FILE = "23/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    links = defaultdict(list)

    with open(IN_FILE) as f:
        for line in f:
            link = line.strip().split("-")
            if link[1] not in links[link[0]]:
                links[link[0]].append(link[1])
                links[link[1]].append(link[0])

    triplets = set()  # use a set to only get unique triplets

    for key in links:
        for pair in combinations(links[key], 2):
            if pair[0] in links[pair[1]] or pair[1] in links[pair[0]]:
                triplet = tuple(sorted([key, pair[0], pair[1]]))
                triplets.add(triplet)

    score = 0
    for triplet in triplets:
        if "t" in [name[0] for name in triplet]:
            score += 1

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
