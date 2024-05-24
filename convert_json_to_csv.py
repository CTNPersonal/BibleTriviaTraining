import json
import csv
import re
import argparse


def json_to_csv(json_file, csv_file):
    # Load JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    header = ["Rank", "Question", "Answer"]

    # Open CSV file for writing
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)

        # Write data
        for entry in data:
            writer.writerow(
                {
                    "Rank": entry["rank"],
                    "Question": entry["question"],
                    "Answer": entry["answer"],
                }
            )


def main():
    parser = argparse.ArgumentParser(description="Convert JSON file to CSV file")
    parser.add_argument(
        "book",
        type=str,
        help="The book of the Bible in json format (e.g., isaiah.json)",
    )
    args = parser.parse_args()
    json_to_csv(f"{args.book}.json", f"csv/{args.book}.csv")


if __name__ == "__main__":
    main()
