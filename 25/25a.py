from time import perf_counter

IN_FILE = "25/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    locks = []
    keys = []

    with open(IN_FILE) as f:
        in_key = False
        in_lock = False
        current = []

        for line in f:
            if in_key:
                if len(line) == 1:
                    in_key = False
                    keys.append(current)
                else:
                    for i in range(len(line)):
                        if line[i] == "#":
                            current[i] += 1
            elif in_lock:
                if len(line) == 1:
                    in_lock = False
                    locks.append(current)
                else:
                    for i in range(len(line)):
                        if line[i] == ".":
                            current[i] -= 1
            else:
                # starting values one beyond expected because need to accomodate the full line at end
                if line[0] == "#":
                    in_lock = True
                    current = [6, 6, 6, 6, 6]
                elif line[0] == ".":
                    in_key = True
                    current = [-1, -1, -1, -1, -1]

        # bs to handle the final item
        if in_key:
            keys.append(current)
        elif in_lock:
            locks.append(current)

    score = 0

    for lock in locks:
        for key in keys:
            valid = True
            for i in range(len(lock)):
                if (lock[i] + key[i]) > 5:
                    valid = False
            if valid:
                score += 1

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
