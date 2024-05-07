import requests
import re
from datetime import datetime, timedelta

url = 'https://api.github.com/repos/MarlinFirmware/Marlin/commits'
response = requests.get(url)
commits = response.json()

# Calculate the date one week ago
one_week_ago = datetime.now() - timedelta(days=70)

with open('output_HTML.txt', 'w') as file:
    file.write('<ul>\n')
    for commit in commits:
        commit_date = datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ')
        if commit_date >= one_week_ago and not commit['commit']['message'].startswith('[cron]'):
            emoji_match = re.search(r'^([^ ]+)', commit['commit']['message'])
            emoji = emoji_match.group(1) if emoji_match else ''
            commit_id_match = re.search(r'\(#(\d+)\)', commit['commit']['message'])
            if commit_id_match:
                commit_id = commit_id_match.group(1)
                description = commit['commit']['message'].split('\n')[0]  # Extract the first line as description
                description = re.sub(r'^[^ ]+ ', '', description)  # Remove emoji
                description = re.sub(r'\s*\([^)]*\)', '', description)  # Remove commit ID
                if not description.startswith(' '):
                    description = f'{emoji} {description}'  # Add space after emoji if missing
                file.write(f'<li>{emoji} <a href="https://github.com/MarlinFirmware/Marlin/pull/{commit_id}">{description}</a></li>\n')
    file.write('</ul>')
