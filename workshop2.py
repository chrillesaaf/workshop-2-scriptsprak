# Csv is a built-in Python library that let us read and write CSV-files
import csv
from collections import defaultdict

# Open salaries.csv, read as an list of dictionary items
# to the variable salaries
with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = list(csv.DictReader(f))

# Create a dictionary where each site maps to a set of weeks
weeks = defaultdict(set)

for row in incidents:
    site = row['site']
    week = row['week_number']
    weeks[site].add(week)

# Convert sets to sorted lists for nicer output
weeks = {site: sorted(weeks) for site, weeks in weeks.items()}

# Show result
for site, weeks in weeks.items():
    print(f'"{site}": {weeks}')