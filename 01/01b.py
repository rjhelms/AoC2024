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

    for x in left:
        # print(x, right.count(x))
        score += x * right.count(x)

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
