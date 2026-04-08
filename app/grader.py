def grade(result, task):
    expected = task["expected"]

    if result == expected:
        return 1.0, "Perfect"

    if len(result) == len(expected):
        return 0.7, "Structure correct"

    if len(result) > 0:
        return 0.3, "Partially correct"

    return 0.0, "Incorrect"