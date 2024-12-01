from time import perf_counter

IN_FILE = "01/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    score = 0
    left = []
    right = []
    with open(IN_FILE) as f:
        for line in f:
            ids = [int(x) for x in line.split()]
            left.append(ids[0])
            right.append(ids[1])

    left.sort()
    right.sort()
    for i in range(len(left)):
        # print(left[i], right[i], abs(right[i] - left[i]))
        score += abs(right[i] - left[i])

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
