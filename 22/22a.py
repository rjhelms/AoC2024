from time import perf_counter

IN_FILE = "22/input.txt"


def mix_prune(new: int, val: int) -> int:
    return (new ^ val) & 16777215


def calc_next(val: int) -> int:
    new = val << 6
    val = mix_prune(new, val)
    new = val >> 5
    val = mix_prune(new, val)
    new = val << 11
    return mix_prune(new, val)


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0

    with open(IN_FILE) as f:
        for line in f:
            val = int(line)
            source = val
            for _ in range(2000):
                val = calc_next(val)
            score += val

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
