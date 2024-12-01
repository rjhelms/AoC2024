IN_FILE = "01/input.txt"

if __name__ == "__main__":
    score = 0
    left = []
    right = []
    with open(IN_FILE) as f:
        for line in f:
            ids = [int(x) for x in line.split()]
            left.append(ids[0])
            right.append(ids[1])

    for x in left:
        print(x, right.count(x))
        score += x * right.count(x)

    print(score)
