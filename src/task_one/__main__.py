from datetime import timedelta, datetime
import ast
import sys


def parse_dates(arr: list[str]) -> list[tuple[datetime, datetime]]:
    return eval(
        compile(
            ast.parse(arr, mode="eval"),
            "",
            "eval",
        )
    )


def decompress_dates(arr: list[tuple[datetime, datetime]]) -> list[datetime]:
    dates = []

    for ranges in arr:
        start, end = ranges
        diff: int = (end - start).days

        for day in range(diff):
            dates.append(start + timedelta(days=day))

    return dates


def main():
    if len(sys.argv) != 2:
        print("Expected list of tuples with date ranges.")
        sys.exit(1)

    try:
        dates = parse_dates(sys.argv[1])
    except Exception as e:
        print("Failed to parse the input data:", e)
        sys.exit(1)

    for date in decompress_dates(dates):
        print(date)


main()
