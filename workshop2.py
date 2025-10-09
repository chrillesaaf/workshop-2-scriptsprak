# Csv is a built-in Python library that let us read and write CSV-files
import csv
from collections import defaultdict

# Helper function to parse Swedish cost format
def parse_swe_cost(cost_str):
    try:
        return float(cost_str.replace(' ', '').replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0

# Open salaries.csv, read as an list of dictionary items
# to the variable salaries
with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = [
        {
            **row,
            'cost_sek': parse_swe_cost(row['cost_sek'])
        }
        for row in csv.DictReader(f)
    ] 
    
    
    list(csv.DictReader(f))

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
report += "---------------------------------------------\n"
report += ('Show sites and analytic period: \n')
report += "---------------------------------------------\n"
for site, weeks in weeks.items():
    report += (f'{site}: {weeks}\n')

# Define the severity levels you want to count
severity_levels = ['critical', 'high', 'medium', 'low']

# Use dictionary comprehension to count each severity
severity_count = {
    level: sum(1 for row in incidents if row['severity'].lower() == level)
    for level in severity_levels
}

# Show result
report += "\n---------------------------------------------\n"
report += ('Incident count by severity:\n')
report += "---------------------------------------------\n"
for level, count in severity_count.items():
    report += (f'{level.capitalize()}: {count}\n')

# Filter incidents where affected_users > 100 using list comprehension
high_incidents = [
    row for row in incidents
    if row['affected_users']. isdigit() and int(row['affected_users']) > 100
]

# Show result
report += "\n---------------------------------------------\n"
report += ('Incidents affecting more than 100 users:\n')
report += "---------------------------------------------\n"
for incident in high_incidents:
    report += (f'- {incident['ticket_id']}: {incident['description']} ({incident['affected_users']} users)\n')

# Sort incidents by cost_sek descending and take top 5
top_5 = sorted(incidents, key=lambda row: row['cost_sek'], reverse=True)[:5]

# Create a dictionary: ticket_id → cost
top_cost_dict = {
    row['ticket_id']: row['cost_sek']
    for row in top_5
}

# Show result
report += "\n---------------------------------------------\n"
report += ('Top 5 most expensive incidents:\n')
report += "---------------------------------------------\n"
for ticket, cost in top_cost_dict.items():
    report += (f'- {ticket}: {cost:.2f} SEK\n')

# write the report to text file
with open('workshop_2.txt', 'w', encoding='utf-8') as f:
    f.write(report)