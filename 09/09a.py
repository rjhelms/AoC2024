from time import perf_counter

IN_FILE = "09/input.txt"

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

    # print(len(file_table))

    start_ptr = 0
    end_ptr = len(file_table) - 1

    while start_ptr < end_ptr:
        if file_table[start_ptr] is not None:
            start_ptr += 1
        elif file_table[end_ptr] is None:
            end_ptr -= 1
        else:
            file_table[start_ptr] = file_table[end_ptr]
            file_table[end_ptr] = None

    score = 0
    for i in range(len(file_table)):
        if file_table[i]:
            score += i * file_table[i]

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
