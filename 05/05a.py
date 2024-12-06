from time import perf_counter
from collections import defaultdict

IN_FILE = "05/input.txt"

AFTER_PAGES = defaultdict(
    list
)  # dictionary of pages with all known pages they come after


def validate_update(update):
    for i in range(len(update)):
        for j in range(i + 1, len(update)):
            if update[j] in AFTER_PAGES[update[i]]:
                # print(AFTER_PAGES[update[i]])
                # print(update[j], " cannot come after ", update[i])
                return False
    return True


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0
    updates = []

    with open(IN_FILE) as f:
        ordering_done = False
        for line in f:
            if not ordering_done:
                if len(line) == 1:
                    ordering_done = True
                else:
                    pages = [int(x) for x in line.split("|")]
                    AFTER_PAGES[pages[1]].append(pages[0])
            else:
                update = [int(x) for x in line.split(",")]
                updates.append(update)

    # print(AFTER_PAGES)

    for update in updates:
        if validate_update(update):
            score += update[int(len(update) / 2)]

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
