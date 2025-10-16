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
summary += '----------------------------------------------------------\n'
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
    summary += "⚠ All sites had at least one critical incident.\n"

# Count how many incidents per severity
severity_count = {
    level: sum(1 for row in incidents if row.get('severity', '').lower() == level)
    for level in severity_levels
}

# Total incidents for percentage calculation
total_incidents = sum(severity_count.values()) or 1

# Calculate average resolution time and cost per severity
severity_stats = {}
for level in severity_levels:
    level_incidents =[row for row in incidents if row.get('severity', '').lower() == level]
    count = len(level_incidents)
    if count > 0:
        avg_resolution = round(sum(row.get('resolution_minutes', 0) for row in level_incidents) / count, 1)
        avg_cost = round(sum(row.get('cost_sek', 0) for row in level_incidents) / count, 1)
        severity_stats[level] = (count, avg_resolution, avg_cost)
    else:
        severity_stats[level] = (0,0,0)

summary += '\nINCIDENTS PER SEVERITY\n'
summary += '---------------------------------------------\n'

for level in severity_levels:
    count, avg_resolution, avg_cost = severity_stats[level]
    percent = (count / total_incidents) * 100
    summary +=(
        f'{level.capitalize():<10}'
        f'{count:3} st {percent:.0f}% - '
        f'Average: {avg_resolution:.0f} min resolution, '
        f"{format_sek(avg_cost)} /incident\n"
    )

summary += '\n\n========================================================================================================\n\n'             
# Add summary before main report
report = summary + report

# write the report to text file
with open('incident_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(report)

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

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

for row in incidents:
    site = row['site']
    severity = row['severity'].lower()

    site_summary[site]['total_incidents'] += 1
    site_summary[site][severity] += 1
    site_summary[site]['resolution_total'] += row['resolution_minutes']
    site_summary[site]['cost_total'] += row['cost_sek']

#Write csv with DictWriter

fieldnames = [
        'site',
        'total_incidents',
        'critical_incidents',
        'high_incidents',
        'medium_incidents',
        'low_incidents',
        'avg_resolution_minutes',
        'total_cost_sek'
    ]

with open('incidents_by_site.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for site, data in site_summary.items():
        avg_resolution = round(data['resolution_total'] / max(1, data['total_incidents']), 2)
        writer.writerow({
            'site': site,
            'total_incidents': data['total_incidents'],
            'critical_incidents': data['critical'],
            'high_incidents': data['high'],
            'medium_incidents': data['medium'],
            'low_incidents': data['low'],
            'avg_resolution_minutes': avg_resolution,
            'total_cost_sek': format_sek(data['cost_total'])
        })

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

def format_sek(amount):
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")

def get_device_type(hostname):
    prefix = hostname[:3].upper()
    if prefix.startswith('SW-'):
        return 'switch'
    elif prefix.startswith('RT-'):
        return 'router'
    elif prefix.startswith('AP-'):
        return 'access_point'
    elif prefix.startswith('FW-'):
        return 'firewall'
    elif prefix.startswith('LB-'):
        return 'load_balancer'
    else:
        return 'unknown'

device_summary ={}

for row in incidents:
    hostname = row['device_hostname']
    if hostname not in device_summary:
        device_summary[hostname] = {
            'site' : row['site'],
            'device_type' : get_device_type(hostname),
            'incident_count' : 0,
            'total_severity' : 0,
            'total_cost' : 0.0,
            'total_affected' : 0,
            'in_last_weeks_warnings' : row.get('previously_flagged', 'no').lower() == 'yes'
        }

    device_summary[hostname]['incident_count'] += 1
    device_summary[hostname]['total_severity'] += float(row.get('impact_score', 0))
    device_summary[hostname]['total_cost'] += float(row.get('cost_sek', 0))
    affected_value = row.get('affected_users', '').strip()
    device_summary[hostname]['total_affected'] += int(affected_value) if affected_value.isdigit() else 0

device_weeks = {}

for row in incidents:
    hostname = row['device_hostname']
    week = int(row['week_number'])
    device_weeks.setdefault(hostname, set()).add(week)

for hostname, data in device_summary.items():
    weeks =device_weeks.get(hostname, set())
    current_week = max(weeks) if weeks else 0
    had_last_week = (current_week - 1) in weeks
    data['in_last_weeks_warnings'] = had_last_week

problem_rows = []
for hostname, data in device_summary.items():
    avg_severity = round(data['total_severity'] / max(1, data['incident_count']), 1)
    avg_affected = round(data['total_affected'] / max(1, data['incident_count']))
    problem_rows.append({
        'device_hostname': hostname,
        'site': data['site'],
        'device_type': data['device_type'],
        'incident_count': data['incident_count'],
        'avg_severity_score': avg_severity,
        'total_cost_sek': format_sek(data['total_cost']),
        'avg_affected_users': avg_affected,
        'in_last_weeks_warnings': 'yes' if data['in_last_weeks_warnings'] else 'no'
    })

fieldnames = [
    'device_hostname', 
    'site', 
    'device_type', 
    'incident_count',
    'avg_severity_score', 
    'total_cost_sek', 
    'avg_affected_users', 
    'in_last_weeks_warnings'
]

with open('problem_devices.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(problem_rows)

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

def format_sek(amount):
    return f"{amount:,.2f}".replace(",", " ").replace(".", ",")

week_summary = defaultdict(lambda: {'total_cost': 0.0, 'total_impact': 0.0, 'count': 0})

for row in incidents:
    week = row.get('week_number', '').strip()
    if not week:
        continue

    cost = row.get('cost_sek', 0.0) or 0.0
    impact = row.get('impact_score', 0.0) or 0.0


    week_summary[week]['total_cost'] += cost
    week_summary[week]['total_impact'] += impact
    week_summary[week]['count'] += 1

cost_rows = []
for week, data in sorted(week_summary.items()):
    avg_impact = round(data['total_impact'] / max(1, data['count']), 2)
    cost_rows.append({
        'week_number': week,
        'total_cost_sek': format_sek(data['total_cost']),
        'avg_impact_score': f"{avg_impact:,.2f}".replace(".", ",")
    })

fieldnames = ['week_number', 'total_cost_sek', 'avg_impact_score']

with open('cost_analysis.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(cost_rows)