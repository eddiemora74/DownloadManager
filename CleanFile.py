import csv
import re


def clean_csv(csv_file):
    lines = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)

    for each in lines:
        each[1] = re.sub("[^a-zA-Z0-9_]+", "", each[1])

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for each in lines:
            writer.writerow(each)
