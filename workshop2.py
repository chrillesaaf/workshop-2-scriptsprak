# Csv is a built-in Python library that let us read and write CSV-files
import csv

# Open salaries.csv, read as an list of dictionary items
# to the variable salaries
with open('network_incidents.csv', encoding='utf-8') as f:
    salaries = list(csv.DictReader(f))