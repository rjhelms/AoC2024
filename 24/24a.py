from time import perf_counter

IN_FILE = "24/input.txt"

# known wires just hold values
KNOWN_WIRES = {}

# unknown wires hold tuple - (first, second, operation)
UNKNOWN_WIRES = {}

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        for line in f:
            if ":" in line:
                line = line.split(':')
                KNOWN_WIRES[line[0]] = int(line[1])
            elif "->" in line:
                line = [x.split() for x in line.split(' -> ')]
                UNKNOWN_WIRES[line[1][0]] = (line[0][0], line[0][2],line[0][1])

    while len(UNKNOWN_WIRES) > 0:
        keys = [x for x in UNKNOWN_WIRES]
        for key in keys:
            # get this wire off the dictionary
            item = UNKNOWN_WIRES.pop(key)
            # if we can't calculate it, put it back
            if item[0] not in KNOWN_WIRES or item[1] not in KNOWN_WIRES:
                UNKNOWN_WIRES[key] = item
                continue

            # otherwise evaluate
            val = 0
            if item[2] == "AND":
                val = KNOWN_WIRES[item[0]] & KNOWN_WIRES[item[1]]
            elif item[2] == "OR":
                val = KNOWN_WIRES[item[0]] | KNOWN_WIRES[item[1]]
            elif item[2] == "XOR":
                val = KNOWN_WIRES[item[0]] ^ KNOWN_WIRES[item[1]]
            KNOWN_WIRES[key] = val

    score = 0
    for key in KNOWN_WIRES:
        if 'z' in key:
            score += KNOWN_WIRES[key] << int(key[1:])
    
    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
