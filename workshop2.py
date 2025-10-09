# Csv is a built-in Python library that let us read and write CSV-files
import csv
from collections import defaultdict

# Open salaries.csv, read as an list of dictionary items
# to the variable salaries
with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = list(csv.DictReader(f))

def swedishNumberStringsToFloat(string):
    # try - try to do something that we know
    # might give us a runtime error / "crash the program"
    try:
        return float(string.replace(' ','').replace(',','.'))
    # handle exceptions - when what we tried didn't work
    except:
        # return 0 if we can't convert to a number
        return 0

# Create a variable that holds our whole text report
report = ""

# Create a dictionary where each site maps to a set of weeks
weeks = defaultdict(set)

for row in incidents:
    site = row['site']
    week = row['week_number']
    weeks[site].add(week)

# Convert sets to sorted lists for nicer output
weeks = {site: sorted(weeks) for site, weeks in weeks.items()}

# Show result
report += ('Show sites and analytic period: \n')
for site, weeks in weeks.items():
    report += (f'"{site}": {weeks}\n')

# Define the severity levels you want to count
severity_levels = ['low', 'medium', 'high', 'critical']

# Use dictionary comprehension to count each severity
severity_count = {
    level: sum(1 for row in incidents if row['severity'].lower() == level)
    for level in severity_levels
}

# Show result
report += ('\nIncident count by severity:\n')
for level, count in severity_count.items():
    report += (f'{level.capitalize()}: {count}\n')

# Filter incidents where affected_users > 100 using list comprehension
high_incidents = [
    row for row in incidents
    if row['affected_users']. isdigit() and int(row['affected_users']) > 100
]

# Show result
report += ('\nIncidents affecting more than 100 users:\n')
for incident in high_incidents:
    report += (f'- {incident['ticket_id']}: {incident['description']} ({incident['affected_users']} users)\n')

# write the report to text file
with open('workshop_2.txt', 'w', encoding='utf-8') as f:
    f.write(report)