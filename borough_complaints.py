import argparse
import csv
from datetime import datetime
from collections import Counter

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input file")
    parser.add_argument("-s", "--start", required=True, help="Start date")
    parser.add_argument("-e", "--end", required=True, help="End date")
    parser.add_argument("-o", "--output", help="Output file")

    return parser.parse_args()


def counter_help(file, start, end):
    count = Counter()
    date = "%m/%d/%Y %I:%M:%S %p"

    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            created = datetime.strptime(row["Created Date"], date)
            if not (start <= created <= end):
                continue

            borough = row["Borough"].strip().title()
            complaint = row["Complaint Type"].strip().lower()

            if borough and complaint:
                count[(complaint, borough)] += 1

    return count

def results(count, outfh):
    writer = csv.writer(outfh)
    writer.writerow(["complaint type", "borough", "count"])
    for (complaint, borough), c in sorted(count.items()):
        writer.writerow([complaint, borough, c])

def main():
    args = parse()
    start = datetime.strptime(args.start, "%Y-%m-%d")
    end = datetime.strptime(args.end, "%Y-%m-%d")

    counts = counter_help(args.input, start, end)

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as outfh:
            results(counts, outfh)
    else:
        import sys
        results(counts, sys.stdout)



if __name__ == "__main__":
    main()