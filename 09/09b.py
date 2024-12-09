from time import perf_counter

IN_FILE = "09/input.txt"

# no need to look at the table after where the last file started
LAST_START_IDX = None


def find_free_space(table: list[int], size: int) -> int | None:
    # returns the starting index of the first free space of the specified size
    # or None if no such space exists

    for i in range(LAST_START_IDX):
        valid_space = True
        for j in range(size):
            if (i + j) >= len(table) or table[i + j] is not None:
                valid_space = False
                break
        if valid_space:
            return i

    return None


def find_file(table: list[int], id: int) -> tuple[int, int] | None:
    # returns a tuple with the starting index and length of the file if found,
    # or None if the file does not exist

    start_idx = None
    end_idx = None

    for i in range(LAST_START_IDX - 1, -1, -1):
        if table[i] == id:
            if end_idx is None:
                end_idx = i
                start_idx = i
            else:
                start_idx = i
        else:
            if end_idx is not None:
                return (start_idx, (end_idx - start_idx) + 1)
        # print(i, start_idx, end_idx)

    # need this case to handle file that starts at index 0 as loop above terminates
    if start_idx is not None and end_idx is not None:
        return (start_idx, (end_idx - start_idx) + 1)
    return None


if __name__ == "__main__":
    start_time = perf_counter()

    file_table = []
    file_id = 0

    with open(IN_FILE) as f:
        is_file = True
        for char in f.read():
            for _ in range(int(char)):
                if is_file:
                    file_table.append(file_id)
                else:
                    file_table.append(None)
            if is_file:
                file_id += 1
            is_file = not is_file

    LAST_START_IDX = len(file_table)

    while file_id > 0:
        if file_id % 100 == 0:
            print(".", end="", flush=True)
        file_id -= 1
        end_ptr, length = find_file(file_table, file_id)
        LAST_START_IDX = end_ptr
        start_ptr = find_free_space(file_table, length)

        # only move to the left
        if start_ptr and start_ptr < end_ptr:
            for i in range(length):
                file_table[start_ptr + i] = file_id
                file_table[end_ptr + i] = None

    score = 0
    for i in range(len(file_table)):
        if file_table[i]:
            score += i * file_table[i]

    print()
    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
