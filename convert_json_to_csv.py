import json
import csv


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
            writer.writerow([item["question"], item["answer"]])


# Convert JSON to CSV
json_to_csv("questions.json", "questions.csv")
