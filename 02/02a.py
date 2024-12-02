from time import perf_counter

IN_FILE = "02/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    reports = []
    score = 0
    with open(IN_FILE) as f:
        for line in f:
            reports.append([int(x) for x in line.split()])

    for report in reports:
        safe = True
        ascending = None
        for i in range(len(report[1:])):
            change = (report[i+1] - report[i])
            if abs(change) < 1 or abs(change) > 3:
                # print("report " + str(report) + " unsafe due to change " + str(change))
                safe = False
                break
            if (change < 0 and ascending == True):
                # print("report " + str(report) + " unsafe due to change to descending")
                safe = False
                break
            elif (change > 0 and ascending == False):
                # print("report " + str(report) + " unsafe due to change to ascending")
                safe = False
                break
            else:
                ascending = (change > 0)
        if safe:
            # print("report " + str(report) + " safe")
            score += 1

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
