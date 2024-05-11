import json
import csv
import re


def json_to_csv(json_file, csv_file):
    # Load JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Open CSV file for writing
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(["Question", "Answer"])

        # Write data
        for item in data["questions"]:
            print(f"Data: {item}")
            question = re.sub(
                r"\([^)]*\)", "", item["question"]
            )  # Remove text in parentheses
            try:
                writer.writerow([question, item["answer"]])
            except Exception as e:
                print(f"Skip missing data for {item} - Error: {e}")


# Convert JSON to CSV
json_to_csv("google_list.json", "google_list.csv")
