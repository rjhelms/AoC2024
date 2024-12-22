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

    prices = []
    changes = []
    i = 0
    print("Calculating prices    ", end="", flush=True)
    with open(IN_FILE) as f:
        for line in f:
            if i % 50 == 0:
                print(".", end="", flush=True)
            i += 1
            val = int(line)
            source = val
            monkey_price = [val % 10]
            monkey_change = []
            for _ in range(2000):
                val = calc_next(val)
                price_change = (val % 10) - monkey_price[-1]
                monkey_price.append(val % 10)
                monkey_change.append(price_change)
            prices.append(monkey_price)
            changes.append(monkey_change)

    print("\nBuilding dictionaries ", end="", flush=True)
    change_dicts = []
    unique_keys = {}
    for i in range(len(prices)):
        if i % 50 == 0:
            print(".", end="", flush=True)
        this_price = prices[i]
        this_change = changes[i]
        change_dict = {}
        for j in range(4, len(this_price)):
            key = tuple(this_change[j - 4 : j])
            val = this_price[j]
            if key not in change_dict:
                change_dict[key] = val
                unique_keys[key] = True
        change_dicts.append(change_dict)

    print("\nEvaluating sequences  ", end="", flush=True)
    best_score = 0
    i = 0

    for key in unique_keys:
        if i % 1250 == 0:
            print(".", end="", flush=True)
        i += 1
        score = sum(score[key] for score in change_dicts if key in score)
        if score > best_score:
            best_score = score

    print()
    print(best_score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
