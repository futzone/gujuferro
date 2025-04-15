import csv

csv_file = "resources/database/trained_files.csv"


def check_if_trained(filename):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == filename:
                return True
    return False


def save_trained_file(filename):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([filename, "timestamp"])
