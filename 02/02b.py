from time import perf_counter

IN_FILE = "02/input.txt"


def check_report(report, errors):
    ascending = None
    for i in range(len(report[1:])):
        change = report[i + 1] - report[i]
        if (
            abs(change) < 1
            or abs(change) > 3
            or (change < 0 and ascending == True)
            or (change > 0 and ascending == False)
        ):
            if errors == 1:
                return False

            if i > 0:
                left_delete = report.copy()
                left_delete.pop(i - 1)
                if check_report(left_delete, 1):
                    return True

            mid_delete = report.copy()
            mid_delete.pop(i)
            if check_report(mid_delete, 1):
                return True

            right_delete = report.copy()
            right_delete.pop(i + 1)
            return check_report(right_delete, 1)
        else:
            ascending = change > 0

    return True


if __name__ == "__main__":
    start_time = perf_counter()

    reports = []
    score = 0
    with open(IN_FILE) as f:
        for line in f:
            reports.append([int(x) for x in line.split()])

    for report in reports:
        if check_report(report, 0):
            score += 1

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
