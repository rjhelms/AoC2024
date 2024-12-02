from time import perf_counter

IN_FILE = "01/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        for line in f:
            pass

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
