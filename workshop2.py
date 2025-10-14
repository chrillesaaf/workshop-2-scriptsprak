# Csv is a built-in Python library that let us read and write CSV-files
import csv
from collections import defaultdict
from collections import Counter

# Helper function to parse Swedish cost format
def parse_swe_cost(cost_str):
    try:
        return float(cost_str.replace(' ', '').replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0

def format_sek(amount):
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",") + " SEK"

with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = [
        {
            **row,
            'site': row['site'],
            'cost_sek': parse_swe_cost(row['cost_sek']),
            'cost_sek_str': format_sek(parse_swe_cost(row['cost_sek'])),
            'resolution_minutes': int(row['resolution_minutes']) if row['resolution_minutes'].isdigit() else 0,
            'severity': row['severity'].lower(),
            'category': row['category'].lower(),
            'impact_score': float(row['impact_score']) if row['impact_score'].replace('.', '', 1).isdigit() else 0.0
        }
        for row in csv.DictReader(f)
    ]


# Open salaries.csv, read as an list of dictionary items
# to the variable salaries
with open('network_incidents.csv', encoding='utf-8') as f:
    incidents = [
        {
            **row,
            'site' :row['site'],
            'cost_sek': parse_swe_cost(row['cost_sek']),
            'cost_sek_str': format_sek(parse_swe_cost(row['cost_sek'])),
            'resolution_minutes': int(row['resolution_minutes']) if row['resolution_minutes'].isdigit() else 0,
            'severity': row['severity'].lower(),
            'category': row['category'].lower(),
            'impact_score': float(row['impact_score']) if row['impact_score'].replace('.','', 1).isdigit() else 0.0
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
report += ('Show sites and analysis period\n')
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
report += ('Incident count by severity\n')
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
report += ('Incidents affecting more than 100 users\n')
report += '---------------------------------------------\n'
for incident in high_incidents:
    report += (
            f"{str(incident['ticket_id']).ljust(15)} "
            f"{incident['site'].ljust(16)}"
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
report += ('Top 5 most expensive incidents\n')
report += '---------------------------------------------\n'
for ticket, cost in top_cost_dict.items():
    report += (f'{ticket}: {format_sek(cost)}\n')

# Calculate total cost using list comprehension + sum
total_cost = sum(row['cost_sek'] for row in incidents)

# Show result
report += '\n---------------------------------------------\n'
report += 'Total cost of all incidents\n'
report += '---------------------------------------------\n'
report += (f'Total cost: {format_sek(total_cost)}\n')

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
report += ('Average resolution time per severity level\n')
report += '---------------------------------------------\n'
for level, avg in avg_resolution.items():
    report += (f'{level.capitalize().ljust(12)} {avg} minutes\n')

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
report += ('Incident overview per site\n')
report += '---------------------------------------------\n'
report += f'{'SITE'.ljust(17)} {'INCIDENTS'.ljust(12)} {'TOTAL COST (SEK)'.ljust(17)} {'AVG RESOLUTION (MIN)'}\n'
for site, data in site_summary.items():
    report += (
        f"{site.ljust(17)} "
        f"{str(data['incident_count']).ljust(12)} "
        f"{format_sek(data['total_cost']).ljust(18)}"
        f"{f'{data['avg_resolution']:.2f}'.ljust(15)}\n"
    )

# Get unique categories
categories = set(row['category'] for row in incidents)

category_summary = {
    cat: round(
        sum(row['impact_score'] for row in incidents if row['category'] == cat) /
        max(1, sum(1 for row in incidents if row['category'] == cat)),
        2
    )
    for cat in categories
}   

report += '\n---------------------------------------------\n'
report += 'Average impact score per category\n'
report += '---------------------------------------------\n'
report += f"{'CATEGORY'.ljust(16)} {'AVG IMPACT SCORE'}\n"

for cat, avg in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
    report += f'{cat.capitalize().ljust(16)} {f'{avg:.2f}'}\n'

# Create a variable that holds our whole text report
summary = ""

summary += '==========================================================\n'
summary += '             INCIDENT ANALYSIS - SEPTEMBER 2024\n'
summary += '==========================================================\n'
summary += 'Analysisperiod: 2024-09-01 to 2024-09-30\n'
total_incidents = sum(severity_count.values())
summary += f'{'Total incidents: '.ljust(12)} {total_incidents}\n'
summary += (f'Total cost: {format_sek(total_cost)}\n')
summary += '\nEXECUTIVE SUMMARY\n'
summary += '--------------------\n'
# Critial devices
critical_incidents = [row for row in incidents if row['severity'] == 'critical']
if critical_incidents:
    from collections import Counter
    device_counts = Counter(row['device_hostname'] for row in critical_incidents)
    worst_device, count = device_counts.most_common(1)[0]
    summary += f"⚠ CRITICAL: {worst_device} has {count} critical incidents (same device that had a warning last week!)\n"
else:
    summary += "✓ No critical incidents this period.\n"

# Most expensive incident
if incidents:
    most_expensive = max(incidents, key=lambda x: x['cost_sek'])
    summary += f"⚠ COST: Most expensive incident: {most_expensive['cost_sek_str']} ({most_expensive['device_hostname']} {most_expensive['category']})\n"

# Recurring problem devices
problem_devices = [row['device_hostname'] for row in incidents if row.get('previously_flagged', '').lower() == 'yes']
unique_problem_devices = len(set(problem_devices))
summary += f"⚠ {unique_problem_devices} devices from last week's 'problem devices' generated new incidents\n"

# Check which sites have no critical incidents
sites = set(row['site'] for row in incidents)
critical_sites = {row['site'] for row in incidents if row['severity'] == 'critical'}

no_critical_sites = sites - critical_sites

if no_critical_sites:
    summary += "✓ POSITIVE: No critical incidents at these sites:\n"
    for site in sorted(no_critical_sites):
        summary += f"  - {site}\n"
else:
    summary += "⚠ All sites had at least one critical incident.\n\n"

# Add summary before main report
report = summary + report

# write the report to text file
with open('report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

# ---------------------------------------------------------------------------------------------------------------------------------
# Initialize summary dictionary

def format_sek(amount):
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")

site_summary = defaultdict(lambda: {
    'total_incidents': 0,
    'critical': 0,
    'high': 0,
    'medium': 0,
    'low': 0,
    'resolution_total': 0,
    'cost_total': 0.0
})

# Populate summary

for row in incidents:
    site = row['site']
    severity = row['severity']

    site_summary[site]['total_incidents'] += 1
    site_summary[site][severity] += 1
    site_summary[site]['resolution_total'] += row['resolution_minutes']
    site_summary[site]['cost_total'] += row['cost_sek']

with open('incidents_by_site.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    writer.writerow([
        'site',
        'total_incidents',
        'critical_incidents',
        'high_incidents',
        'medium_incidents',
        'low_incidents',
        'avg_resolution_minutes',
        'total_cost_sek'
    ])

    for site, data in site_summary.items():
        avg_resolution = round(data['resolution_total'] / max(1, data['total_incidents']), 2)
        writer.writerow([
            site,
            data['total_incidents'],
            data['critical'],
            data['high'],
            data['medium'],
            data['low'],
            avg_resolution,
            round(data['resolution_total'] / max(1, data['total_incidents']), 2),
            format_sek(data['cost_total'])
        ])
