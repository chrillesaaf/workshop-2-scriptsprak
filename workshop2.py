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
            'site' :row['site'],
            'cost_sek': parse_swe_cost(row['cost_sek']),
            'resolution_minutes': int(row['resolution_minutes']) if row['resolution_minutes'].isdigit() else 0,
            'severity': row['severity'].lower()
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
report += f"{'SITE'.ljust(20)} {'WEEKS ANALYZED'}\n"
for site, weeks_list in weeks.items():
    formatted_weeks = ", ".join(weeks_list)
    report += f"{site.ljust(20)} {formatted_weeks}\n"

# Define the severity levels you want to count
severity_levels = ['critical', 'high', 'medium', 'low']

# Use dictionary comprehension to count each severity
severity_count = {
    level: sum(1 for row in incidents if row['severity'].lower() == level)
    for level in severity_levels
}

# Show result
report += '\n---------------------------------------------\n'
report += ('Incident count by severity:\n')
report += '---------------------------------------------\n'
report += f"{'SEVERITY'.ljust(12)} {'COUNT'}\n"
for level, count in severity_count.items():
    report += (
        f'{level.capitalize().ljust(12)} {count}\n')

# Filter incidents where affected_users > 100 using list comprehension
high_incidents = [
    row for row in incidents
    if row['affected_users']. isdigit() and int(row['affected_users']) > 100
]
high_incidents = sorted(high_incidents, key=lambda row: row['affected_users'], reverse=True)

# Show result
report += '\n---------------------------------------------\n'
report += ('Incidents affecting more than 100 users:\n')
report += '---------------------------------------------\n'
for incident in high_incidents:
    report += (
            f"{str(incident['ticket_id']).ljust(15)} "
            f"{incident['site'].ljust(13) }"
            f"{str(incident['affected_users'])} affected users\n"
    )

# Sort incidents by cost_sek descending and take top 5
top_5 = sorted(incidents, key=lambda row: row['cost_sek'], reverse=True)[:5]

# Create a dictionary: ticket_id → cost
top_cost_dict = {
    row['ticket_id']: row['cost_sek']
    for row in top_5
}

# Show result
report += '\n---------------------------------------------\n'
report += ('Top 5 most expensive incidents:\n')
report += '---------------------------------------------\n'
for ticket, cost in top_cost_dict.items():
    report += (f'- {ticket}: {cost:.2f} SEK\n')

# Calculate total cost using list comprehension + sum
total_cost = sum(row['cost_sek'] for row in incidents)

# Show result
report += '\n---------------------------------------------\n'
report += 'Total cost of all incidents:\n'
report += '---------------------------------------------\n'
report += (f' {total_cost:.2f} SEK\n')

# Calculate average resolution time per severity
avg_resolution = {
    level: round(
        sum(row['resolution_minutes'] for row in incidents if row['severity'] == level) / 
        max(1, sum(1 for row in incidents if row['severity'] == level)),
        2
    )
    for level in severity_levels
}

# Show result
report += '\n---------------------------------------------\n'
report += ('Average resolution time per severity level:\n')
report += '---------------------------------------------\n'
for level, avg in avg_resolution.items():
    report += (f'{level.capitalize()}: {avg} minutes\n')

# Get unique sites
sites = set(row['site'] for row in incidents)

# Build summary per site
site_summary = {
    site: {
        'incident_count': sum(1 for row in incidents if row['site'] == site),
        'total_cost': round(sum(row['cost_sek'] for row in incidents if row['site'] == site), 2),
        'avg_resolution': round(
            sum(row['resolution_minutes'] for row in incidents if row['site'] == site) /
            max(1, sum(1 for row in incidents if row['site'] == site)),
            2
        )
    }
    for site in sites
}

# Show result
report += '\n---------------------------------------------\n'
report += ('Incident overview per site:\n')
report += '---------------------------------------------\n'
report += f"{'SITE'.ljust(17)} {'INCIDENTS'.ljust(12)} {'TOTAL COST (SEK)'.ljust(18)} {'AVG RESOLUTION (MIN)'}\n"
for site, data in site_summary.items():
    report += (
        f"{site.ljust(17)} "
        f"{str(data['incident_count']).ljust(12)} "
        f"{f'{data['total_cost']:.2f}'.ljust(18)} "
        f"{str(data['avg_resolution']).ljust(15)}\n"
    )



# write the report to text file
with open('workshop_2.txt', 'w', encoding='utf-8') as f:
    f.write(report)
