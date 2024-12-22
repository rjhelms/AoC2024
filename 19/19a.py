from time import perf_counter

IN_FILE = "19/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        lines = f.readlines()
        patterns = [x.strip() for x in lines[0].split(',')]
        designs = [x.strip() for x in lines[2:]]
    # print(patterns)
    # print(designs)

    score = 0
    for design in designs:
        candidate_patterns = [x for x in patterns if x in design]
        candidate_patterns.sort(key=len, reverse=True)
        open_set = ['']
        while len(open_set) > 0:
            check_design = open_set.pop()
            for pattern in candidate_patterns:
                new_pattern = check_design + pattern
                if new_pattern == design:
                    # print('\t', new_pattern)
                    score += 1
                    break
                elif new_pattern == design[:len(new_pattern)]:
                    open_set.append(new_pattern)
            else:
                open_set.sort(key=len)
                # print(design, len(open_set), open_set[-1] if len(open_set) > 0 else '')
                continue
            break

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
