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

    groups = []

    for key in links:
        group = {key}
        for device in links[key]:
            new_group = group.copy()
            in_group = True

            # iterate through the existing group, and see if this device is paired with them all
            for item in group:
                if item not in links[device]:
                    in_group = False
                    break
            if in_group:
                new_group.add(device)
            group = new_group

        if group not in groups:
            groups.append(group)

    groups.sort(key=len)
    longest = sorted(list(groups.pop()))

    string = ""
    for key in longest:
        string += key
        string += ","

    print(string[:-1])

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
